# This file is only to provide the helper functions to viz.ipynb
# 
#
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
        df = df.drop(columns=['name','run_name','run_type','repetitions','repetition_index','family_index','per_family_instance_index','threads'])
        df['library'] = df['library'].str[3:]

        df.insert(0, 'library', df.pop('library'))
        df.insert(1, 'sampleNumber', df.pop('sampleNumber'))
        return df
    else:
        print('specify a benchmark path')

def appendFFTMflops(dataFrame):
    '''
    appends MFLOPS column according to FFTW's scaling with MFLOPS = 5*N*log_2(N) / time
    -----------------
    dataFrame <pd dataframe>: of the benchmark data
    '''
    cpu_time = dataFrame['cpu_time'].astype(float)
    N = dataFrame['sampleNumber'].astype(float)
    MFLOPS = np.divide(np.multiply(5*N,np.log2(N)),cpu_time)
    dataFrame['MFLOPS'] = MFLOPS

    return dataFrame



def plotBenchmark(dataFrame, libraries=['all'], property='cpu_time', isLog = True, size = [5,5], plotTitle = ''):
    '''
    plots a property of the benchmark accross the sample numbers for each specified library.
    -----------------
    dataFrame <pd dataframe>: of the benchmark data
    libraries <string>: the library names you want to test
    property <string>: the property to be plotted in the y-axis
    isLog <bool>: sets the y axis to be logarithmic
    size: figure size parameter
    plotTitle <string>: sets the plot title
    '''

    #setting libraries
    if(libraries[0] == 'all'):
        libraries = pd.unique(dataFrame['library'])
        print('plotting all libraries')
    else:
        templib = []
        for lib in libraries:
            if(lib in pd.unique(dataFrame['library'])):
               templib.append(lib)
            else:
                print(lib + ' not found in dataframe')
        libraries = templib

    #plot styling
    plt.rc('font',family='Times New Roman')
    plt.style.use('fivethirtyeight')
    
    fig, ax = plt.subplots(figsize=size)

    #plotting
    for lib in libraries:
        libData = dataFrame[dataFrame['library'] == lib]
        y = libData[property].astype(float)
        samples = libData['sampleNumber'].astype(int)
        ax.plot(samples, y, marker='.')

    #figure adjustments
    ax.legend(libraries,bbox_to_anchor=(0, 1.02, 1, 0.2), loc="lower left",
                mode="expand", borderaxespad=0, ncol = 3)
    ax.set_xscale('log', base=2)
    if(isLog):
        ax.set_yscale('log')
    
    if(plotTitle != ''):
        ax.set_title(plotTitle)
    ax.set_xlabel('Samples')
    ax.set_ylabel(property)
    
    return fig

def benchRank(dataFrame, property='cpu_time', rankRange = [2,14]):
    '''
    Ranks the libraries according to a certain property
    '''

    dataFrame['sampleNumber'] = pd.to_numeric(dataFrame['sampleNumber'])
    dataFrame['cpu_time'] = pd.to_numeric(dataFrame[property])
    rankedData = dataFrame.sort_values(by=['sampleNumber',property])

    samples = [2**rankRange[0],2**rankRange[1]]
    rankedData = rankedData.loc[(rankedData['sampleNumber'] >= samples[0]) & (rankedData['sampleNumber'] <= samples[1])][['sampleNumber','library','cpu_time','real_time','time_unit']]

    return rankedData
