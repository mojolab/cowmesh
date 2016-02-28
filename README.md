# COWMesh - Community OWned Mesh Networks
## Tools for community owned communication meshes

--------------------------------------------------

	 -/          -\-
	 -||-       -||- 
	 -\\-       -//-  
	  _|||||||||||_
	 / /         \ \
	/-/|(0) | (0)|\-\
	   |         |
		|   |   |
		 |o | o|
		 -------
			(|)
         
-------------------------------------------------------
While working with different kind of peer driven communication networks we realized that we need more tools that 
enable cross platform and corss network meshing. 

This toolset strives to collate tools that enale such cross network sharing. 

We assume two additional layers to the traditional seven in the OSI model, i.e. the peer layer and the user layer that go on either side of the application layer.  

###Stateful Systems
At the very base level all communicating objects are communicating a particular state to each other. This is the basis for interaction on the COWMesh


###States

A state is a condition that is transient, held by an object at a given time. In order to articulate and express the state, a State object is needed. The State object should not be confused with the state.
The state itself at any given time is stored in a predefined location. The predefined location is communicated to the State object via a configuration file or similar construct. 
The State object then accesses the state and based on it and the configuration of the Stateful system reports and updates the status based on interactions that it has with the external world, via Interfaces exposed in Different Contexts

###Interfaces
A mechanism for a Stateful system to expose some or all of its State to another System

###Context
A Stateful system may not wish to use the same Interfaces or expose the same State to all other Systems. Context is a construct that allows a Stateful system to define boundaries to its exposure to other systems. 

###
