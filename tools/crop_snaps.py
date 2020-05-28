#!/usr/bin/env python
import numpy as np
from netCDF4 import Dataset

def add_bool_arg(parser, name, default=False):
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--' + name, dest=name, action='store_true')
    group.add_argument('--no_' + name, dest=name, action='store_false')
    parser.set_defaults(**{name:default})

def process_command_line_args():
    # Basic command-line interface for static-2D plotting
    import argparse

    parser = argparse.ArgumentParser(description='Remove snaps from the end of a dataset')

    parser.add_argument("-n", "--start",
                        default=0,
                        type=int,
                        help="Start of slice (default first snap)"
                        )
    
    parser.add_argument("-m", "--finish",
                        default=-1,
                        type=int,
                        help="Finish of slice (default last snap)"
                        )
                        
    parser.add_argument("-f", "--filepath",
                        default=None,
                        type=str,
                        required=True,
                        help="Full filepath to top-level run directory"
                        )

    parser.add_argument("-i", "--input",
                        default="snaps",
                        type=str,
                        help="Prefix of nc files to be trimmed",
                        )
    
    add_bool_arg(parser, 'overwrite_temp', default=False)
    add_bool_arg(parser, 'dry_run', default=False)

    args = parser.parse_args()

    return args

if __name__=="__main__":
    import os
    from shutil import copyfile
    import time
    from os import rename, mkdir
    from os.path import join, exists
    
    current_time = time.strftime("%Y.%m.%d-%H:%M:%S", time.gmtime())
    backup_dir = 'crop_{}'.format(current_time)
    
    args = process_command_line_args()
    filepath = args.filepath
    
    # Automatically prepend filepath to filename
    fullpath = lambda file: join(filepath, file)
    # Check if a file exists in the directory
    file_exists = lambda file: exists(fullpath(file))
    
    # Open snaps00000.nc to find the current length of snaps
    assert(file_exists("snaps00000.nc"))
    snaps_metadata = Dataset(fullpath("snaps00000.nc"))
    length_before = snaps_metadata.nsnaps_last
    # Convert to 1-indexing for snaps
    snaps_before = np.arange(length_before)+1
    
    start_slice = args.start
    if args.finish < 0:
        finish_slice = snaps_before[args.finish]
    else:
        finish_slice = args.finish
    
    snaps_after = np.array(snaps_before[start_slice:finish_slice])
    print("Snaps slice to extract")
    print("Snaps (1-indexed) = ", snaps_after)
    
    # Convert back to 0-indexing for slices
    slice_indices = snaps_after - 1
    write_indices = np.arange(len(slice_indices))
    snaps_metadata.close()
    
    # Process each snap in the directory matching input
    snaps_in_dir = 0
    input_snaps = []
    output_snaps = []
    
    for filename in os.listdir(args.filepath):
        if filename.startswith(args.input) and filename.endswith(".nc"):
            input_snaps.append(filename)
            snaps_in_dir += 1
    
    print("\n{} snaps found to process\n".format(snaps_in_dir))
    for filename in input_snaps:
        output_snap = join(backup_dir, filename)
        output_snaps.append(output_snap)
        print("Will move {} to {} and overwrite {} with cropped snaps".format(filename, output_snap, filename))
    
    input_diags = []
    output_diags = []
    for diag in {"diagnostics_scalar.nc", "diagnostics_zonal.nc"}:
        if file_exists(diag):
            output_diag = join(backup_dir, diag)
            input_diags.append(diag)
            output_diags.append(output_diag)
            print("\n{} found".format(diag))
            # print("Will move {} to {} and overwrite {} with cropped diags".format(diag, output_diag, diag))
            print("Will move {} to {}".format(diag, output_diag))
        else:
            print("\n{} not found".format(diag))

    tau_handle = Dataset(input_snaps[0])
    tau = np.copy(tau_handle['tau'])
    tau_handle.close()
    
    tau_start = tau[slice_indices[0]]
    tau_end = tau[slice_indices[-1]]
    print("Will crop to tau range {:3.4e} to {:3.4e}".format(tau_start, tau_end))
    
    if args.dry_run:
        print("\ndry_run: exiting")
        exit()
    else:
        print("\nEntering processing loop\n")
    
    mkdir(join(filepath, backup_dir))
    
    # Process diagnostics (need to trim to same time range, depsite being over a different time interval)
    for filename, backup in zip(input_diags, output_diags):
        print("Processing {}, backing up to {}".format(filename, backup))
        rename(fullpath(filename), fullpath(backup))
        
        source_data = Dataset(fullpath(backup), 'r')
        dest_data = Dataset(fullpath(filename), 'w')
        
        # tau is defined differently between the two diagnostic files
        if filename == "diagnostics_scalar.nc":
            tau_diags = source_data["diags"][:, 0]
        elif filename == "diagnostics_zonal.nc":
            tau_diags = source_data["tau"][:]
            
        diag_length_before = source_data.ndiag_last
        # Convert to 1-indexing for diags
        diag_before = np.arange(diag_length_before)+1
        
        start_diag = np.searchsorted(tau_diags, tau_start, side='left')
        finish_diag = np.searchsorted(tau_diags, tau_end, side='right')
        print("{} cropped to {} - {}".format(filename, start_diag, finish_diag))
        
        diag_after = np.array(diag_before[start_diag:finish_diag])
        # print("diag slice to extract")
        # print("diag (1-indexed) = ", diag_after)
        
        # Convert back to 0-indexing for slices
        diag_indices = diag_after - 1
        diag_write_indices = np.arange(len(diag_indices))
        
        dest_data.ndiag_last = len(diag_indices)
        dest_data.tau_last = tau_diags[diag_indices[-1]]
        
        dest_data.crop_time = current_time
        dest_data.start_crop = diag_indices[0]
        dest_data.finish_crop = diag_indices[-1]
        
        dest_data.createDimension('dim_time', None)
        dest_data.createDimension('dim_nvars', source_data.dimensions['dim_nvars'].size)
        
        # Set attributes
        if filename == "diagnostics_scalar.nc":
            dest_data.diag_size = source_data.diag_size
            
        elif filename == "diagnostics_zonal.nc":
            dest_data.createDimension('dim_nrho', source_data.dimensions['dim_nrho'].size)
            dest_data.diag_zonsize = source_data.diag_zonsize
            dest_data.nrho = source_data.nrho
        
        # Set variables
        for varname, var in source_data.variables.items():
            variable_data = dest_data.createVariable(varname,"f8",var.dimensions)
            
            for attrname in var.ncattrs():
                variable_data.setncattr(attrname, var.getncattr(attrname))
            
            assert(variable_data.dimensions[0] == 'dim_time')
            
            if len(variable_data.dimensions) == 1:
                variable_data[diag_write_indices] = var[diag_indices]
            elif len(variable_data.dimensions) == 2:
                variable_data[diag_write_indices, :] = var[diag_indices, :]
            elif len(variable_data.dimensions) == 3:
                variable_data[diag_write_indices, :, :] = var[diag_indices, :, :]
        
        dest_data.close()
        source_data.close()
    
    # Process snaps
    for filename, backup in zip(input_snaps, output_snaps):
        print("Processing {}, backing up to {}".format(filename, backup))
        rename(fullpath(filename), fullpath(backup))

        source_data = Dataset(fullpath(backup), 'r')
        dest_data = Dataset(fullpath(filename), 'w')
        
        dest_data.vgrid_nl = source_data.vgrid_nl
        dest_data.perpghost_nl = source_data.perpghost_nl
        dest_data.nsnaps_last = len(slice_indices)
        
        dest_data.crop_time = current_time
        dest_data.start_crop = slice_indices[0]
        dest_data.finish_crop = slice_indices[-1]
        
        dest_data.createDimension('dim_tau', None)
        dest_data.createDimension('dim_vgrid', source_data.dimensions['dim_vgrid'].size)
        dest_data.createDimension('dim_perpghost', source_data.dimensions['dim_perpghost'].size)
        
        for varname, var in source_data.variables.items():
            variable_data = dest_data.createVariable(varname,"f8",var.dimensions)
            
            for attrname in var.ncattrs():
                variable_data.setncattr(attrname, var.getncattr(attrname))
            
            assert(variable_data.dimensions[0] == 'dim_tau')
            
            if len(variable_data.dimensions) == 1:
                variable_data[write_indices] = var[slice_indices]
            elif len(variable_data.dimensions) == 2:
                variable_data[write_indices, :] = var[slice_indices, :]
            
        source_data.close()
        dest_data.close()
    