#!/bin/bash

SCRIPT_PATH=.

python -W ignore library_plot.py -params plot_parameters.csv -parts part_information.csv -designs dna_designs.csv -regulation reg_information.csv -output order_orientation_library.pdf
