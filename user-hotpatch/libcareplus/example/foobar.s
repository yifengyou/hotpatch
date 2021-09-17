	.file	"foo.c"
#---------- var ---------
	.text
	.section	.rodata
.LC0:
	.string	"Hello world!"
#---------- func ---------
	.globl	print_hello
	.text
	.globl	print_hello
	.type	print_hello, @function
print_hello:
.LFB0:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	leaq	.LC0(%rip), %rdi
	call	puts@PLT
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0:
	.size	print_hello, .-print_hello
print_hello.Lfe:
#---------- kpatch begin ---------
	.pushsection .kpatch.text,"ax",@progbits
	.globl	print_hello.kpatch
	.globl	print_hello.kpatch
	.type	print_hello.kpatch, @function
print_hello.kpatch:
.LFB0.kpatch:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
	leaq	.LC0.kpatch(%rip), %rsi
	leaq	.LC1.kpatch(%rip), %rdi
	movl	$0, %eax
	call	printf@PLT
	nop
	popq	%rbp
	.cfi_def_cfa 7, 8
	ret
	.cfi_endproc
.LFE0.kpatch:
	.size	print_hello.kpatch, .-print_hello.kpatch
print_hello.kpatch_end:
	.popsection

	.pushsection .kpatch.strtab,"a",@progbits
kpatch_strtab1:
	.string "print_hello.kpatch"
	.popsection
	.pushsection .kpatch.info,"a",@progbits
print_hello.Lpi:
	.quad print_hello
	.quad print_hello.kpatch
	.long print_hello.Lfe - print_hello
	.long print_hello.kpatch_end - print_hello.kpatch
	.quad kpatch_strtab1
	.quad 0
	.long 0
	.byte 0, 0, 0, 0
	.popsection

#---------- kpatch end -----------
#---------- func ---------
	.globl	main
	.globl	main
	.type	main, @function
main:
.LFB1:
	.cfi_startproc
	pushq	%rbp
	.cfi_def_cfa_offset 16
	.cfi_offset 6, -16
	movq	%rsp, %rbp
	.cfi_def_cfa_register 6
.L3:
	call	print_hello
	movl	$1, %edi
	movl	$0, %eax
	call	sleep@PLT
	jmp	.L3
	.cfi_endproc
.LFE1:
	.size	main, .-main
	.pushsection .kpatch.text,"ax",@progbits
	.section .kpatch.data,"aw",@progbits
.LC0.kpatch:
	.string	"being patched"
	.popsection
	.pushsection .kpatch.data,"aw",@progbits
.LC1.kpatch:
	.string	"Hello world %s!\n"
	.popsection
	.ident	"GCC: (Ubuntu 7.5.0-3ubuntu1~18.04) 7.5.0"
	.section	.note.GNU-stack,"",@progbits
