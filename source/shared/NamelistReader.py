from source import Path, defaultdict, os
import f90nml
# Fortran namelist reader, using f90nml module
# The resulting Params object may be indexed like a dictionary to access
# namelist groups, which are returned as "defaultdict" objects. These are
# identifical to dictionaries, except that upon access of a missing element they
# return [] instead of raising a keyError. This can tidy up checking of default
# values

class NamelistReader:
    
    def __init__(self, namelist_dict):
        assert(type(namelist_dict) is dict)
        self.namelist_dict = namelist_dict
    
    @staticmethod
    def cleaned_read(filename):
        # Signed floats are not read correctly
        # Replace "+" with a " " empty string
        with open(filename, 'r') as nml_file:
            contents = nml_file.read()
            if "+" in contents:
                # Safe read with "+" character
                contents = contents.replace("+", " ")

                with open(filename.name+'_cleaned', 'w') as nml_file_cleaned:
                    nml_file_cleaned.write(contents)

                # Read the cleaned filename
                namelist = f90nml.read(filename.name+'_cleaned')

                # Remove the cleaned filename
                os.remove(filename.name+'_cleaned')
                return namelist.todict()
        
        namelist = f90nml.read(filename)
        return dict(namelist.todict())
    
    def __str__(self):
        return_string = ""
        
        for group, dictionary in dict(self.namelist_dict).items():
            return_string += "{} \n".format(group)
            for key, value in dict(dictionary).items():
                return_string += "    {:<25s} = {} \n".format(key, value)

        return return_string
    
    def __getitem__(self, key):
        # Note that elements in the namelist are switched to lowercase
        # The 'defaultdict' will return [] if the element is missing, which can
        # be then replaced by default value
        return defaultdict(list, self.namelist_dict[key.lower()])
    