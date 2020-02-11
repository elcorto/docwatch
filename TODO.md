config file
-----------
* If needed, add more specialized converter classes derived from
  PandocConverter, e.g. PandocToFooConverter. In case we don't want to pass
  e.g. filters as option for all converters, we can add a section

      [PandocToFooConverter]
      filters =
          aaa
          bbb

  which replace (or append to??) the filters in [DEFAULT], if any.
