import m5
import m5.objects
# print(dir(m5.objects))
from m5.objects import *

# 1.Create System
system = System()

#set clock and volt
system.clk_domain = SrcClockDomain()
system.clk_domain.clock = '1GHz'
system.clk_domain.voltage_domain = VoltageDomain()

# Set up memory mode. 'timing'required for pipelined and cache
system.mem_mode = 'timing' 
system.mem_ranges = [AddrRange('512MB')]

# Create RISC-V CPU
system.cpu = RiscvMinorCPU()
# Create Caches
class L1Cache(Cache):
    tag_latency = 4
    data_latency = 4
    response_latency = 1
    mshrs = 16
    tgts_per_mshr = 20

class L1ICache(L1Cache):
    #originally64
    size = '32kB'
    assoc = 8
    is_read_only = True

class L1DCache(L1Cache):
    size = '32kB'
    #assoc = 4
    #add victim cache
    assoc = 32
    #increase mshr
    mshrs = 16
    tgts_per_mshr = 20

class L2Cache(Cache):
    size = '256kB'
    assoc = 8
    tag_latency = 5
    data_latency = 5
    response_latency = 2
    mshrs = 20
    tgts_per_mshr = 12
    #default in L2 for 
    replacement_policy = BIPRP()
    #prefetcher = StridePrefetcher()

class L3Cache(Cache):
    size = '512kB'          # small banks
    assoc = 2            # High associativity to reduce conflict misses
    tag_latency = 20      # Slower than L2
    data_latency = 20
    response_latency = 20
    mshrs = 20
    tgts_per_mshr = 12
    #replacement_policy = RandomRP()
    # do tagged with fetching the next 4 block
    #prefetcher = TaggedPrefetcher(degree=4, latency=1)





#instantiate caches
system.cpu.icache = L1ICache()
system.cpu.dcache = L1DCache()
system.l2cache = L2Cache()
#system.l3cache = L3Cache()
system.l3cache = [L3Cache(size='512kB') for i in range(4)]

# Connect Caches as Hierarchy: CPU -> L1 -> L2 bus -> L2 cache -> L3 bus -> L3 cache -> memory
#buses set-up
system.l2bus = L2XBar()
#additional features for banked L3 caches
system.l3bus = CoherentXBar()
system.l3bus.width = 64
system.l3bus.frontend_latency = 10  
system.l3bus.forward_latency = 10   
system.l3bus.response_latency = 1  
system.l3bus.snoop_response_latency = 1  

system.membus = SystemXBar()




#connections
#CPU -> L1
system.cpu.icache.cpu_side = system.cpu.icache_port
system.cpu.dcache.cpu_side = system.cpu.dcache_port

#L1 -> L2 bus
system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports

#L2 bus -> L2 cache-> L3 buses
system.l2cache.cpu_side = system.l2bus.mem_side_ports
system.l2cache.mem_side = system.l3bus.cpu_side_ports

#L3 Bus -> L3 Cache -> memory
#system.l3cache.cpu_side = system.l3bus.mem_side_ports
#system.l3cache.mem_side = system.membus.cpu_side_ports
for i in range(4):
    system.l3cache[i].cpu_side = system.l3bus.mem_side_ports
    system.l3cache[i].mem_side = system.membus.cpu_side_ports
    system.l3cache[i].addr_ranges = [AddrRange(
        start=0, 
        size='512MB',          # The cache "covers" the whole range...
        intlvHighBit=7,        # ...but only listens to specific bits.
        intlvBits=2,           # 2 bits (log2(4 banks)) are used for selection.
        intlvMatch=i           # Bank 0 takes '00', Bank 1 takes '01', etc.
    )]

# Create the Interrupt Controller (Required for RISC-V)
system.cpu.createInterruptController()
#interrupt ports omitted interrupt ports connections for simple SE mode)

# Create the Memory Controller
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

#Syscall Emulation
process = Process()


#change file path here
# path to the compiled binary
process.cmd = ['/Users/jackhsiao/Documents/ece401/RISV_MESI/gem5/configs/tutorial/stream_2MB'] 
system.workload = SEWorkload.init_compatible(process.cmd[0])
system.cpu.workload = process
system.cpu.createThreads()

#Instantiate the Simulation
root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning simulation!")
exit_event = m5.simulate()

print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")