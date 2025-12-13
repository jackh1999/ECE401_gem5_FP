# ECE401_gem5_FP
Using GEM5 for Cache optimizations under RISCV MinorCPU

If you have not downloaded GEM5, please refer to its website and scon it in classical set-up.


Benchmarks are stream.c and stream_64byte.c which are already configured by riscv gnu toolchain as stream_2MB and stream_64; we run all experiments under both Benchmarks.
- Note the Benchmarks both require long time to simulate; do test_rv64 (object of test.c) for pure functionality check.
- Also you can glimpse the results through the stats.txt files in the data directory

Running file is done by ./build/ALL/gem5.opt ./desired_file_path

Experiment Procedures:
1. We will be first check whether our banked L3 cache emulation is more authentic in terms of miss penalties/latencies: although the setup of these two emulations are almost irrelevant to our current baseline and best designs, the only differentiation as banked/unbanked L3 cache makes it decent to expose if there are extra latency under banked L3 cache setup.

    risv_pipeline_3_caches vs. premodified riscv_pipeline_L3banked_L2mod (can revisit by implementing banked L3 in risv_pipeline_3_caches)
3. MSHR and high associativity are mostly done through sweeping corresponding parameters in the fundamental baseline design until reaching the current baseline; we need to highlight that we obey the physical limits of status quo caches, and we partially refer our cache parameters to some of GEM5 default boards and examples.

   Sweeping through modulating parameters in riscv_pipeline_baseline; compare riscv_pipeline_baseline vs. riscv_pipeline_assoc
5. With/without Victim cache is implemented when stride prefetcher is implemented since we will be using stride prefetcher in our best design. We do want to stress that intuitive victim cache comparison is also done but not shown here for succinctness.

   tuning riscv_pipeline_vc for initial check; modify riscv_pipeline_L3banked_L2mod with/without victim caches
7. Replacement policies are compared in sequences of L1/L2/L3 as Random/Random/Random versus LRU/LRU(BIP)/LRU in the final/best set-up and Default/Random/Random versus Default/Random/Random shown in replacement policy comparison subsection.

   tuning in riscv_pipeline_rp for sanity check; tuning riscv_pipeline_L3banked_L2mod for best case scenario
9. Prefetchers are compared among each other for better performance; they are run under implementations of higher associativity and victim cache.

   Tuning riscv_pipeline_L3banked_L2mod with different prefetcher setups
11. Run riscv_pipeline_best under both Benchmarks to compare with riscv_pipeline_baseline.
