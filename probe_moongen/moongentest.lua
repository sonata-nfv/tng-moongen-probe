local mg     = require "moongen"
local memory = require "memory"
local device = require "device"
local ts     = require "timestamping"
local filter = require "filter"
local hist   = require "histogram"
local stats  = require "stats"
local timer  = require "timer"
local arp    = require "proto.arp"
local log    = require "log"


local ffi = require "ffi"


-- set addresses here
local DST_MAC		= "a0:36:9f:69:6c:fa" -- resolved via ARP on GW_IP or DST_IP, can be overriden with a string here
local SRC_IP_BASE	= "10.0.0.10" -- actual address will be SRC_IP_BASE + random(0, flows)
local DST_IP		= "10.1.0.10"
local SRC_PORT		= 1234
local DST_PORT		= 319



mytime = 10

-- answer ARP requests for this IP on the rx port
-- change this if benchmarking something like a NAT device
local RX_IP		= DST_IP
-- used to resolve DST_MAC
local GW_IP		= DST_IP
-- used as source IP to resolve GW_IP to DST_MAC
local ARP_IP	= SRC_IP_BASE


local C = ffi.C

file = io.open("testluafile.txt", "a")
io.output(file)


function configure(parser)
	parser:description("Generates UDP traffic and measure latencies. Edit the source to modify constants like IPs.")
	parser:argument("txDev", "Device to transmit from."):convert(tonumber)
	parser:argument("rxDev", "Device to receive from."):convert(tonumber)
        parser:argument("time", "Test time."):convert(tonumber)
	parser:argument("bandwidth", "Test bandwidth."):convert(tonumber)
	parser:option("-r --rate", "Transmit rate in Mbit/s."):default(15):convert(tonumber)
	parser:option("-f --flows", "Number of flows (randomized source IP)."):default(0):convert(tonumber)
	parser:option("-s --size", "Packet size."):default(1300):convert(tonumber)
end



function master(args)
        --mytime = args.time
	txDev = device.config{port = args.txDev, rxQueues = 3, txQueues = 3}
	rxDev = device.config{port = args.rxDev, rxQueues = 3, txQueues = 3}
	device.waitForLinks()
	-- max 1kpps timestamping traffic timestamping
	-- rate will be somewhat off for high-latency links at low rates
	if args.rate > 0 then
		txDev:getTxQueue(0):setRate(args.bandwidth)
		txDev:getTxQueue(1):setRate(1)
                print (args.rate - (args.size + 4) * 8 / 1000)

	end


	--rxDev:getTxQueue(0).dev:UdpGenericFilter(rxDev:getRxQueue(2))

	mg.startTask("loadSlave", txDev:getTxQueue(0), rxDev, args.size, args.flows, txDev, args)
	mg.startTask("timerSlave", txDev:getTxQueue(1), rxDev:getRxQueue(1), args.size, args.flows, args)

	mg.startTask("receiveSlave", rxDev:getRxQueue(2), args.size, args)




	--arp.startArpTask{
		-- run ARP on both ports
	--	{ rxQueue = rxDev:getRxQueue(2), txQueue = rxDev:getTxQueue(2), ips = RX_IP },
		-- we need an IP address to do ARP requests on this interface
	--	{ rxQueue = txDev:getRxQueue(2), txQueue = txDev:getTxQueue(2), ips = ARP_IP }
	--}
	mg.waitForTasks()
        io.close(file)
end

local function fillUdpPacket(buf, len)
	buf:getUdpPacket():fill{
		ethSrc = "A0:36:9F:69:6C:F8",
		ethDst = DST_MAC,
		ip4Src = SRC_IP,
		ip4Dst = DST_IP,
		udpSrc = SRC_PORT,
		udpDst = DST_PORT,
		pktLength = len
	}
end


function loadSlave(queue, rxDev, size, flows, txDev, args)


	-- retrieve the number of xstats on the recieving NIC
    -- xstats related C definitions are in device.lua
    local numxstats = 0
    local xstats = ffi.new("struct rte_eth_xstat[?]", numxstats)

    -- because there is no easy function which returns the number of xstats we try to retrieve
    -- the xstats with a zero sized array
    -- if result > numxstats (0 in our case), then result equals the real number of xstats
    local result = C.rte_eth_xstats_get(rxDev.id, xstats, numxstats)
    numxstats = tonumber(result)





	local mempool = memory.createMemPool(function(buf)
		fillUdpPacket(buf, size)
	end)
	local bufs = mempool:bufArray()
        print ("ARGSTIME")
        print (args.time)
	local runtime = timer:new(args.time)
        local counter = 0
	local txCtr = stats:newDevTxCounter(queue, "csv", "tx.csv")
	local rxCtr = stats:newDevRxCounter(rxDev, "csv", "rx.csv")
	local txCtr2 = stats:newDevTxCounter(queue, "plain")
        local rxCtr2 = stats:newDevRxCounter(rxDev, "plain")
	local baseIP = parseIPAddress(SRC_IP_BASE)
        local myusefulcounter = 0
        local pktCtr = stats:newPktTxCounter("Packets counted", "csv", "pktcounterTX.csv")
	while mg.running() and (not runtime or runtime:running()) do
		bufs:alloc(size)
		for i, buf in ipairs(bufs) do
			local pkt = buf:getUdpPacket()
			pkt.ip4.src:set(baseIP + counter)
			counter = incAndWrap(counter, flows)
                        -- log:info("OMG FFS")
			pktCtr:countPacket(buf)
                        myusefulcounter = myusefulcounter + 1
		end
		-- UDP checksums are optional, so using just IPv4 checksums would be sufficient here
		bufs:offloadUdpChecksums()
		queue:send(bufs)
		txCtr:update()
		rxCtr:update()
		txCtr2:update()
                rxCtr2:update()
		pktCtr:update()
	end
	pktCtr:finalize()
	txCtr:finalize()
        rxCtr:finalize()
	txCtr2:finalize()
	rxCtr2:finalize()

	local stats3 = pktCtr:getStats()
    for key,value in pairs(stats3) do log:info(tostring(key) .. " - " .. tostring(value)) end


	log:info(green("---------------------Moongen TX STATS---------------------------"))
    local stats = txCtr:getStats()
    for key,value in pairs(stats) do log:info(tostring(key) .. " - " .. tostring(value)) end

    log:info(green("---------------------Moongen RX STATS---------------------------"))

    local stats2 = rxCtr:getStats()
    for key,value in pairs(stats2) do log:info(tostring(key) .. " - " .. tostring(value)) end

    log:info(green("------------------------TX DEV STATS--------------------------------"))
    log:info(tostring(myusefulcounter))
    local txStats = txDev:getStats()
    log:info("ipacktes: " .. tostring(txStats.ipackets))
    log:info("opacktes: " .. tostring(txStats.opackets))
    log:info("ibytes: " .. tostring(txStats.ibytes))
    log:info("obytes: " .. tostring(txStats.obytes))
    log:info("imissed: " .. tostring(txStats.imissed))
    log:info("ierrors: " .. tostring(txStats.ierrors))
    log:info("oerrors: " .. tostring(txStats.oerrors))
    log:info("rx_nombuf: " .. tostring(txStats.rx_nombuf))
    log:info("q_ipacktes[0]: " .. tostring(txStats.q_ipackets[0]))
    log:info("q_ipacktes[1]: " .. tostring(txStats.q_ipackets[1]))
    log:info("q_ipacktes[2]: " .. tostring(txStats.q_ipackets[2]))
    log:info("q_ipacktes[3]: " .. tostring(txStats.q_ipackets[3]))

    log:info(green("------------------------RX DEV STATS--------------------------------"))
    log:info(tostring(myusefulcounter))
    local rxStats = rxDev:getStats()
    log:info("ipacktes: " .. tostring(rxStats.ipackets))
    log:info("opacktes: " .. tostring(rxStats.opackets))
    log:info("ibytes: " .. tostring(rxStats.ibytes))
    log:info("obytes: " .. tostring(rxStats.obytes))
    log:info("imissed: " .. tostring(rxStats.imissed))
    log:info("ierrors: " .. tostring(rxStats.ierrors))
    log:info("oerrors: " .. tostring(rxStats.oerrors))
    log:info("rx_nombuf: " .. tostring(rxStats.rx_nombuf))
    log:info("q_ipacktes[0]: " .. tostring(rxStats.q_ipackets[0]))
    log:info("q_ipacktes[1]: " .. tostring(rxStats.q_ipackets[1]))
    log:info("q_ipacktes[2]: " .. tostring(rxStats.q_ipackets[2]))
    log:info("q_ipacktes[3]: " .. tostring(rxStats.q_ipackets[3]))





-- if no xstats are available we will skip them
    if numxstats > 0 then
        xstats = ffi.new("struct rte_eth_xstat[?]", numxstats)
        C.rte_eth_xstats_get(rxDev.id, xstats, numxstats)
        xstatNames = ffi.new("struct rte_eth_xstat_name[?]", numxstats)
        C.rte_eth_xstats_get_names(rxDev.id, xstatNames, numxstats)
        log:info(green("------------------------XSTATS-------------------------------"))
        log:info("Number of xstats: " .. numxstats)
        for i=0,result-1 do
		if xstats[i].value ~= 0 then
	               log:info(ffi.string(xstatNames[i].name, 64) .. ": " .. tostring(xstats[i].value))
                       io.write(tostring(xstatNames[i].name) .. ": " .. tostring(xstats[i].value) .. "\n")
		end
        end
    else
        log:warn("This device does not provide any xstats")
    end



end

function timerSlave(txQueue, rxQueue, size, flows, args)
	if size < 84 then
		log:warn("Packet size %d is smaller than minimum timestamp size 84. Timestamped packets will be larger than load packets.", size)
		size = 84
	end
	local timestamper = ts:newUdpTimestamper(txQueue, rxQueue)
	local hist = hist:new()
	mg.sleepMillis(20) -- ensure that the load task is running
	local counter = 0
	local rateLimit = timer:new(0.01)
	local runtime = timer:new(args.time)
	local baseIP = parseIPAddress(SRC_IP_BASE)
	local pktCtr2 = stats:newPktTxCounter("Packets counted", "csv", "pktcounterTIME.csv")
	while mg.running() and (not runtime or runtime:running()) do
		hist:update(timestamper:measureLatency(size, function(buf)
			fillUdpPacket(buf, size)
			local pkt = buf:getUdpPacket()
			pkt.ip4.src:set(baseIP + counter)
			counter = incAndWrap(counter, flows)
			pktCtr2:countPacket(buf)
		end))
		pktCtr2:update()
		rateLimit:wait()
		rateLimit:reset()
	end
	pktCtr2:finalize()
	-- print the latency stats after all the other stuff
	mg.sleepMillis(300)
	hist:print()
	hist:save("histogram.csv")
end


function receiveSlave(rxQueue, size, args)
    log:info(green("Starting up: ReceiveSlave"))

    local mempool = memory.createMemPool()
    local rxBufs = mempool:bufArray()
	local runtime = timer:new(args.time)
    -- this will catch a few packet but also cause out_of_buffer errors to show some stats
    while mg.running() and (not runtime or runtime:running()) do
        rxQueue:tryRecvIdle(rxBufs, 1)
        rxBufs:freeAll()
    end
end