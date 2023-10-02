import yaml 
import h5py
import numpy as np 

class Save: 
    """
    _summary_

    Args:
        collection_instance (deepbench.collection.Collection): Instance of a collection to save
        save_path (str): Directory to save to
    """
    def __init__(self, collection_instance, save_path) -> None:
        self.objects = collection_instance.objects
        self.params = collection_instance.object_params 
        self._clean_params()
        self.save_path = save_path
        

    def _save_parameters(self): 
        with open(f"{self.save_path.rstrip('/')}/dataset_parameters.yaml", 'w') as f:
            yaml.safe_dump(self.params, f)

    def _clean_params(self): 
        for key in self.params: 
            for subkey in self.params[key]: 
                if "tolist" in dir(self.params[key][subkey]): 
                    self.params[key][subkey] = self.params[key][subkey].tolist() 

    def _save_h5(self):
        object_array = np.array(list(self.objects.values()), dtype=np.float32)
        f = h5py.File(f"{self.save_path.rstrip('/')}/dataset.h5",'w')

        f.create_dataset('data',data=object_array,dtype=np.float32)
        f.close()

    def __call__(self, format):
        options={
            "h5":self._save_h5
        }
        if format not in options.keys(): 
            raise NotImplementedError

        options[format]()
        self._save_parameters()