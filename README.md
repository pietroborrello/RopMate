# ROPMate

ROPMate is a prototype visual ROPChain builder that assists the attacker in composing the chain with the desired semantics. ROPMate lets the user to filter and select gadgets to add to his chain, while presenting to him only the gadgets that fits the semantics and guarantees he wants. The user is also able to search for similar gadgets with respect to the selected one, needing the same semantics, but different guarantees.

![alt text](/RopMate_paper/ropmate-screen.png "ROPMate Screenshot")

### View A (Tree View)
This is the Main View: it provides the whole list of analyzed gadgets. Filters and controls apply to such list to restrict the search space. The gadgets in the main view are hierarchically ordered by class, and then by parameters that represents their semantic meaning. 

Near an opened category, an histogram is displayed, indicating to the user the number of gadgets of each class, to quickly give an hint on the overall view.

Click on a gadget to have further informations on it.

### View B (Analysis View)
The analysis view offers an insight of the selected gadget, it shows gadget attributes and offers the user the possibility to add the gadget to the chain or to search for similar gadgets. This is done by collecting all the gadget in the tree with the same semantics, and plotting them in a graph based their different modified register when executing. 

This allows the user to search for gadgets with the same effect but that clobber different registers. Clicking on a displayed point will show the class of gadget in the tree view to visualize them.

### View C (Chain View)
The chain view presents the current state of the builded chain. Adding a gadget to the chain will trigger the recomputation for the registers the user has successfully set with the chain, and, by default, the view of the whole gadgets will display only the gadgets safe with respect to modified registers, that the user can choose.

Each gadget in the chain has a unique color based on the register it semantically sets.
Additionally, for every gadget his dependencies are computed, and a slot on each gadget is displayed with the colors matching the register it depends on. The lenght of the slot encodes if the dependency is satisfied and set (short) or not (long) by previous gadgets. A dependency is a register that must be properly set to execute the gadget correctly, as a dereferenced or read register.

The chain view offers the possibility to move gadgets in the chain by dragging and dropping, and to remove them. Once the user is happy with the built chain clicking Dump the system will generate a python script to integrate with current exploit technologies that will generate the byte-code of the chain.

### View D (Control Panel)

The control panel allows the user to perform additional filtering on the gadget displayed. He is able to select which registers should be preserved in the gadget listing, to let the user safely choose gadget without clobbering registers set in the chain. The user has also the possibility to ask the system to display only gadgets that don't access memory (apart from the stack obviously) to be able to choose simpler gadgets first.

### View E (Filter View)

The filter view, jointly with the control panel, is used by the user to reduce the number of gadgets displayed, therefore to further simplify the research. The user is allowed to explicitly define the exact gadgets semantics he is searching for, for example "rax++". Writing a plain register will show all the gadgets that semantically set such register.


## Install
```
pip3 install flask
pip3 install pandas
pip3 install numpy
pip3 install scipy
pip3 install scikit-learn
```

## Run

The Tool is meant to be run locally, by default it opens a predetermined database of gadgets. Details on the back-end server that performs the gadget analysis will be released.

```
python3 server.py
```
