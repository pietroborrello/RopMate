# ROPMate

ROPMate is the first Visual Analytics system specifically designed to assist human in composing  ROP chains with a desired semantics.

In contrast, previous ROP tools typically require users to inspect a puzzle of hundreds or thousands of lines of textual information, making it a daunting task. 

ROPMate presents users with a clear interface of well-defined and semantically meaningful gadgets. The system supports incrementally building exploits by suggesting gadget candidates filtered according to constraints on preserved registers and accessed memory. Several visual aids are offered to identify suitable gadgets and assemble them into semantically correct chains.

The user is also able to search for similar gadgets with respect to a selected one, needing the same semantics, but different constraints.

![alt text](/images/main.png "ROPMate Screenshot")

### View C (Tree View)
This is the Main View: it provides the whole list of analyzed gadgets. Filters and controls apply to such list to restrict the search space. The gadgets in the main view are hierarchically ordered by class, and then by operations that represents their semantic meaning. 

Near an opened class, an histogram is displayed, indicating to the user the number of gadgets of each operations, to quickly give an hint on the overall view.

Gadgets are ordered by ascending complexity. Each gadget has an associated *memory requirement* bar
on its right; the width of the bar represents the space in the stack required by the gadget to work properly. The color of the bar encodes the stack occupation with respect to a memory threshold.

A *dereferenced registers matrix* is aligned to the right of the gadgets and shows the registers used
to access the memory; each column represents a register that may be dereferenced. Each entry of the matrix is filled by a rectangle if the gadget dereferences the register (suggesting that the register has to be properly set to safely use it to access the memory). The rectangle has a full height if the condition is not currently satisfied by the chain and it has half height otherwise. 

Click on a gadget to have further informations on it.

### View D and E (Analysis Views)
The analysis view offers an insight of the selected gadget, it shows gadget attributes and offers the user the possibility to add the gadget to the chain or to search for similar gadgets. This is done by collecting all the gadget in the tree with the same semantics, and plotting them in a graph based their different modified register when executing. 

This allows the user to search for gadgets with the same effect but that clobber different registers. Clicking on a displayed point will show the class of gadget in the tree view to visualize them.

### View F (Chain View)
The chain view presents the current state of the builded chain. Adding a gadget to the chain will trigger the recomputation for the registers the user has successfully set with the chain, and, by default, the view of the whole gadgets will display only the gadgets safe with respect to modified registers, that the user can choose.

Each gadget in the chain has a unique color based on the register it semantically sets.
Additionally, for every gadget his dependencies are computed, and a slot on each gadget is displayed with the colors matching the register it depends on.
A dependency is a register that must be properly set to execute the gadget correctly and can be distinguished between dereferenced registers dependency (on the left of the rectangle) and source registers dependency (on the right) that represent registers used by the gadget to implement a particular operation.
The lenght of the slot encodes if the dependency is satisfied and set (short) or not (long) by previous gadgets.

The chain view offers the possibility to move gadgets in the chain by dragging and dropping, and to remove them. Once the user is happy with the built chain clicking Dump the system will generate a python script to integrate with current exploit technologies that will generate the binary encoding of the chain.

### View B (Registers Pane)

The control panel allows the user to perform additional filtering on the gadget displayed. The user is able to select which registers should be preserved in the gadget listing, for example to safely choose gadgets without clobbering registers already set in the chain. 

The user has also the possibility to ask the system to display only gadgets that don't access memory (apart from the stack obviously) to be able to choose simpler gadgets first.

### View A (Filter View)

The filter view, jointly with the Registers Pane, is used by the user to reduce the number of gadgets displayed, therefore to further simplify the research. The user is allowed to explicitly define the exact gadgets semantics he is searching for, for example `rax++` or `rax = rax + rbx` (unfortunately need to pay attention to set spaces properly). Writing a plain register, as `rax`, will show all the gadgets that semantically set such register. Writing a star before a plain register, as `*rax`, will show all the gadgets that semantically write or read memory through such register. The query language is now limited and will be expanded in the future.


## Install
```
pip install flask
pip install pandas
pip install numpy
pip install scipy
pip install scikit-learn
```

## Run

The Tool is meant to be run locally, by default it opens a predetermined database of gadgets. Details on the back-end server that performs the gadget analysis will be released. You will be able to analyze your own binaries soon! Examples of analyzed binaries are included in the `files` folder.

```
python server.py
```

Will start the server that will provide the interface on `localhost:5000`
 
