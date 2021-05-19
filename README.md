# yaml2svd

This is for now a tiny script to automate SVD creation for custom HDL cores. 

This allows us to use & reuse memory mapped cores with their register access description

You could then use, say, `svd2rust`, or [Renode](https://renode.io/about/) (untested)

The example core contains one GPIO and UART based on [VexRiscv](https://github.com/SpinalHDL/VexRiscv) implementation, and one custom peripheral.

## example usage

```shell
$ pip install -r requirements.txt
$ python3 yaml2svd.py example-core/top.yaml example-core/CORE_NAME.yaml
```



This software is provided as is, mainly because i didn't test it further than the example core. You are welcome to do a PR if you improve it in any way.