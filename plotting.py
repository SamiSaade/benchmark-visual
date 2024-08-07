# This file is only to provide the helper functions to viz.ipynb
# 
#
import json
import pandas as pd
import matplotlib.pyplot as plt

def benchmarkParse(path = 'path/to/benchmark.json'):
    '''
    Parses the benchmark json into a pandas dataset with the library names and sample numbers detached and cleaned
    -----------------
    path <string>: path of the benchmark's path/to/benchmark.json file
    '''
    if(path != 'path/to/benchmark.json'):
        with open(path, 'r') as f:
            json_data = json.load(f)

        df = pd.json_normalize(json_data, 'benchmarks')
        df[['library', 'sampleNumber']] = df['name'].str.split('/', expand=True)
        df = df.drop(columns=['name','run_name','run_type','repetitions','repetition_index'])
        df['library'] = df['library'].str[3:]

        df.insert(0, 'library', df.pop('library'))
        df.insert(1, 'sampleNumber', df.pop('sampleNumber'))
        return df
    else:
        print('specify a benchmark path')


def plotBenchmark(dataFrame, libraries=['all'], property='cpu_time', isLog = True, plotTitle = ''):
    '''
    plots a property of the benchmark accross the sample numbers for each specified library.
    -----------------
    dataFrame <pd dataframe>: of the benchmark data
    libraries <string>: the library names you want to test.
    property <string>: the property to be plotted in the y-axis
    isLog <bool>: sets the y axis to be logarithmic
    plotTitle <string>: sets the plot title
    '''

    #grouping data by unique library name
    dataLibs = dataFrame.groupby('library')[property].unique()
    samplesLibs = dataFrame.groupby('library')['sampleNumber'].unique()
    fig, ax = plt.subplots(figsize=[10, 6])

    #plotting all libraries
    if(libraries[0] == 'all'):
        print('plotting all libraries')
        for lib in dataLibs.keys():
            time = dataLibs[lib].astype(float)
            samples = samplesLibs[lib].astype(int)
            ax.plot(samples, time, marker='.', ls=':')
        ax.legend(dataLibs.keys())

    #plotting select libraries
    else:
        removeLib = []
        for lib in libraries:
            if(lib in dataLibs.keys()):
                time = dataLibs[lib].astype(float)
                samples = samplesLibs[lib].astype(int)
                ax.plot(samples, time, marker='.', ls=':')
            else:
                print(lib + ' not found in dataset')
                removeLib.append(lib)
        for lib in removeLib:
            libraries.remove(lib)
        ax.legend(libraries)

    #figure adjustments
    ax.set_xscale('log', base=2)
    if(isLog):
        ax.set_yscale('log')
    ax.set_xticks(samplesLibs[0].astype(int))
    ax.set_title(plotTitle)
    ax.set_xlabel('Samples')
    ax.set_ylabel('CPU Time (ns)')
    
    return fig