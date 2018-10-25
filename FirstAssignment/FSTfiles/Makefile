.PHONY: all compile graph pdf clean

all: compile graph pdf

compile:
	@echo "1. compiling FST"
	fstcompile --isymbols=timextractor.isyms --osymbols=timextractor.osyms --keep_isymbols --keep_osymbols timextractor.fst.txt timextractor.fst

graph:
	@echo "2. drawing graphical representation"
	fstdraw timextractor.fst timextractor.dot

pdf:
	@echo "3. converting graph to PDF"
	dot -Tpdf timextractor.dot > timextractor.pdf

clean:
	@echo "cleaning up files"
	rm -f *.fst *.dot *.pdf
