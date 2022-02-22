#!/usr/bin/env python

## Code for correcting fish IDs (stupidly)
# Written by Ammon Perkes for use in the laskowski lab
# For questions contact Ammon at perkes.ammon@gmail.com

## Assumes there are 4 IDs or else things might get weird

## Be careful! If anything goes wrong this can delete your data, make sure you're not running this on your only copy...
import numpy as np
import os
import sys


def clean_inf(x):
    x[x == np.inf] = np.nan
    x[x == -np.inf] = np.nan
    return x

## Read in 4 files
source_folder = sys.argv[1]
npz_files = sorted(os.listdir(source_folder))

## Check to make sure there aren't more than 4 or less than 0
if len(npz_files) > 4:
    raise Exception("Too many fish in directory")
if len(npz_files) == 0:
    raise Exception("No files in target directory")

## Calculate the center point of each fish
x_means,y_means = [],[]
for i in range(len(npz_files)):
    in_file = npz_files[i]
    f = np.load(f'{source_folder}/{in_file}')
    
    xs = np.array(f['X'])
    ys = np.array(f['Y'])
    xs = clean_inf(xs)
    ys = clean_inf(ys)
    x_mean,y_mean = np.nanmean(xs),np.nanmean(ys)
    x_means.append(x_mean)
    y_means.append(y_mean)


## Correct by the center point
y_means = np.array(y_means)
if len(npz_files) == 4:
    x_means = x_means - np.nanmean(x_means)
    y_means = y_means - np.nanmean(y_means)
## If there are fewer than 4 fish, this needs to be a global center to make sense.
else:
    x_means = x_means - CENTER[0]
    y_means = y_means - CENTER[1]

## Check which coordinate is which
coords = [-1,-2,-3,-4]
for i in range(len(npz_files)):
    if x_means[i] < 0:
        if y_means[i] < 0:
            coords[i] = 0
        else:
            coords[i] = 2
    else:
        if y_means[i] < 0:
            coords[i] = 1
        else:
            coords[i] = 3

vals,counts = np.unique(coords,return_counts=True)
if max(counts) > 1:
    raise Exception('Two fish assigned to same quadrant')

## Rename (temporarily to prevent conlicts.)
new_names = []
newer_names = []

for i in range(len(npz_files)):
    old_name = npz_files[i]
    new_name = old_name.replace(str(i) + '.npz',str(coords[i])) + 'tmp.npz'
    new_names.append(new_name)
    newer_names.append(new_name.replace('tmp.npz','.npz'))
    src = f"{source_folder}/{old_name}"
    dst = f"{source_folder}/{new_name}"
    os.rename(src,dst)

## Drop the 'tmp' to get the final file names
for i in range(len(npz_files)):
    old_name = new_names[i]
    new_name = newer_names[i]
    src = f"{source_folder}/{old_name}"
    dst = f"{source_folder}/{new_name}"
    os.rename(src,dst)
