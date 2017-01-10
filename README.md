This repository contains project - "Disambiguation of Polysemous Queries for Document Retrieval".

Read Me:
1. Instructions for setup
Assuming the Linux set-up is equipped with python and Perl installations (if not follow instructions on Google to install respective packages):
1.1 WordNet :
This package is required by multiple components of the software. Download link for the same is given below:
*insert link here*
Make sure the extracted folder is in the Home folder.
1.2 WordNet: Similarity:
	This package consists all the perl packages required to calculate semantic relatedness using WordNet. The Download and Installation is given on the following site: 	

	Follow the instruction given on the site for setting up WordNet: Similarity along with its pre-requisites. Make sure all the installations are in the Home folder. 
1.3 NLTK
Install NLTK by following instructions on the given site
http://www.nltk.org/install.html
Once installed copy the nltk_data folder, attached herewith, into the Home folder.
1.4 tomcat
Install tomcat from the following site:
*insert site for tomacat*
1.5 Solr
Download Solr form the link given below:
*insert site for solr download*
Follow instruction given on the following site for the installation:
       *insert site for installation*
       The above site also contain instruction to add text documents to Solr. 
The setup procedure for Solr may lead to man errors accrding to system configuration. These errors are to be solved one by one by referring to Google and trying different solutions suggested on the Internet. If any difficulties any of the above set up please contact any of the project members.

Once all the setup is completed copy the codes present in the Programs folder attached herewith into Home/WordNet: Similarity (version)/ samples folder on your  system. 
Follow the instructions below to execute the code:
1. Run the python code “disamb_final.py”  present in the samples folder.
2. Enter an ambiguous query
3. Copy the expanded query from the terminal to the query input of Solr
4. Hit execute query to extract the documents.  
