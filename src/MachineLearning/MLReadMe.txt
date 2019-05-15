ML Read Me

Should be used in this order 

	-ontologyToTagMap.py
		-main 
			-expects a json file in the folder inputOntology
			-creates tag_map.json in MLfiles directory 

	-get_training_data.py
		-main 
			-expects tag_map.json from above, training_data.json to be in MLfiles (our file. not generated. should already be there)
			-creatses curr_training_data.json in MLfiles


	-tagger.py
		-main
			-expects	
				-tag_map.json in MLfiles 
				-curr_training_data.json in MLfiles
				-all csv's it needs to run ML on to be in inputData directory 
			-creates new csv copys of the old ones with a new row on top with ML given header with old name and an index I belive saved into MLOutputdata





	-train_tagger.py IGNORE 




