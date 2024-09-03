# Benchmark Visualization for [fft-biquad-benchmark](https://github.com/jbr-smtg/fft-biquad-benchmark)

A small tool to visualize the benchmark.json data obtained from the FFT and Biquad benchmark. You can plot, tabulate, and rank and export them into pdf or latex format. 
_This was used as in my dissertation with Steinberg Media Technologies GmbH at Queen Mary University_

### How to visualize your benchmark data:

1. Clone the repository
2. Run <code>pip install -r requirements.txt</code> to install needed libraries
3. Use the following flags <code>--benchmark_out=path/to/benchmark.json</code> and <code>--benchmark_out_format=json</code> when running the benchmark executable in [fft-biquad-benchmark](https://github.com/jbr-smtg/fft-biquad-benchmark)
4. Copy your benchmark files into this project's directory (preferrably in the benchmarks folder)
5. Follow along viz.ipynb in order to parse in the data, clean it, tabulate it, and plot it accordingly
