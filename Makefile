check:
	mdl --style=.mdlrc.rb *.md
	rozental --ban_obscene_words --reorder_vocabulary .
