config file
-----------
* If needed, add more specialized converter classes derived from
  PandocConverter, e.g. PandocToFooConverter. In case we don't want to pass
  e.g. filters as option for all converters (which we do currently in the
  `[DEFAULT]` section), we can add a section

      [PandocToFooConverter]
      filters =
          aaa
          bbb

  to replace (or append to??) the filters in `[DEFAULT]`.

source file format
------------------
For source files other than pandoc's markdown (default markdown flavor in
pandoc) such as `gfm`, `markdown_strict`, `commonmark`, or in general all
formats that pandoc cannot detect automatically, we may need to add an `-f` flag
to pass to pandoc. Alternatively, add the option to pass any extra options to
pandoc.

error handling
--------------
* In PandocConverter, we pipe all stdout and stderr to logfile. That deals with
  all errors from pandoc and filters. So far so good.
* Deal w/ exceptions raised in threads (e.g. from cv.convert()). Right now that
  prints to terminal and messes up vim. Or maybe move cv.convert() back to main
  thread :)
