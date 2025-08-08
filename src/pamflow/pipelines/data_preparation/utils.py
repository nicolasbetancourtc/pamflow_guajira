import os
from pathlib import Path
from os import listdir


#%%
def find_wav_files(folder_path, recursive=False):
    """ Search for files with wav or WAV extension """
    wav_files = []
    if recursive:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.lower().endswith('.wav'):
                    wav_files.append(os.path.join(root, file))
    else:
        for file in os.listdir(folder_path):
                    if file.lower().endswith('.wav'):
                        wav_files.append(os.path.join(folder_path, file))
    
    # Transform the list of strings to a list of Path objects
    wav_files = [Path(path) for path in wav_files]
    
    return wav_files
def add_file_prefix(folder_name: str, recursive:bool=False, verbose:bool=False) -> None:
    """
    Adds a prefix to the file names in the given directory.
    The prefix is the name of the immediate parent folder of the files.

    Parameters:
    folder_name(str): Name of directory which contains files.
    recursive(bool): If True, searches for files in sub-directories recursively.
                     Defaults to False if not provided.

    Returns: None
    """
    folder_path = Path(folder_name)

    # Get list of files to process
    flist = find_wav_files(folder_path, recursive=recursive)
    
    # remove hidden files 
    flist = [f for f in flist if not f.name.startswith('.')]

    if verbose:
        print(f'Number of WAVE files detected: {len(flist)}')

    # remove files that already have the parent directory name
    flist = [f for f in flist if (not f.name.startswith(f.parent.name+'_'))]

    # Loop and change names
    if verbose:
        print(f'Number of WAVE files detected with no prefix: {len(flist)}')
        print('Renaming files...')
    
    flist_changed = list()
    for fname in flist:
        prefix = fname.parent.name
        new_fname = fname.with_name(f'{prefix}_{fname.name}')
        try:
            fname.rename(new_fname)
            flist_changed.append(str(new_fname))
        except Exception as e:
            print(f"Error occurred while renaming {fname}: {e}")
    
    if verbose:
        print('Process completed!')
        print(f'Number of WAVE files renamed: {len(flist_changed)}')
        
    return flist_changed