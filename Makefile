WHAT_TO_PRINT = "Lorem Ipsum"
LS_OUTPUT = $(shell ls)

ifeq ($(WHAT_TO_PRINT), "Lorem Ipsum")
	PRINT_THIS = "Lorem Ipsum"
else
	PRINT_THIS = "Hello World!"
endif

print-hello-world:
	@echo "Hello World"

print-hello-world-again: print-hello-world
	@echo "Hello World Again"

print-makro:
	@echo $(WHAT_TO_PRINT)

print-ls-output:
	@echo $(LS_OUTPUT)

print-if-else:
	@echo $(PRINT_THIS)