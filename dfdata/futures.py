import importlib




def save_futures_contract(
    source,
    db_name=None,
    table_name=None,
    #is_unify=False, 是否为同一格式
):   
    """   
    保存期货合约表
    
    输入数据源，默认保存该数据源期货合约表。

    Parameters：
        source (str): 数据源名称
        db_name (str): 数据库名称
        
    Returns:
        None
        
    See Also：
        read_futures_contract()
        
    Notes:
        笔记
        
    Examples:
        save_futures_contract(source="tushare")
    """
    
    module_source_name = "dfdata.source."+source
    module_source = importlib.import_module(module_source_name)
    
    print(module_source)
    module_source.futures.save_futures_contract(db_name)
    
    
def read_futures_contract(
    
):
    print("read")