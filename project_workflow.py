"""
with annotations for yesWorkflow visualization
"""

""" @BEGIN project_workflow
@IN nypl_menus_dirty @URI directory:nypl_menus_dirty/
@OUT nypl_menus_clean  @URI directory:nypl_menus_clean/
@OUT initial_profile @URI file:initial_profile.png
@OUT initial_usecase_query @URI file:initial_usecase_query.csv
@OUT ic_violations_before @URI file:ic_violations_before.png
@OUT nypl_menus_2  @URI directory:nypl_menus_2/
@OUT diff_summary  @URI file:diff_summary.png/
@OUT ic_violations_after @URI file:ic_violations_after.png
@OUT clean_usecase_query @URI file:clean_usecase_query.csv
"""

""" @BEGIN proccess_w_OpenRefine @desc clean syntactical errors and flag duplicates 
@IN nypl_menus_dirty  @URI directory:nypl_menus_dirty/
@OUT nypl_menus_1  @URI directory:nypl_menus_1/
@END OpenRefine
"""

""" @BEGIN initial_profiling @desc provide statistics about data prior to cleaning and usecase query results
@IN nypl_menus_dirty  @URI directory:nypl_menus_dirty/
@OUT initial_profile @URI file:initial_profile.png
@OUT initial_usecase_query @URI file:initial_usecase_query.csv
@END initial_profiling
"""

""" @BEGIN csv2db @desc loads npyl menu csv files into sqlite db
@IN nypl_menus_1  @URI directory:nypl_menus_1/
@OUT database @URI file:database.db
"""
"""@END csv2db"""

"""@BEGIN check_integrity_constraints @desc log violations and visualize statistics
@IN database @URI file:database.db
@OUT violations_log @URI file:violations_log.csv
@OUT ic_violations_before @URI file:ic_violations_before.png
"""
"""@END check_integrity_constraints"""


"""@BEGIN enforce_integrity_constraints @desc correct database.db for violations 
@IN violations_log @URI file:violations_log.csv
@IN database @URI file:database.db
@OUT nypl_menus_2  @URI directory:nypl_menus_2/
@OUT ic_violations_after @URI file:ic_violations_after.png
"""
"""@END enforce_integrity_constraints"""


"""@BEGIN compare_updates @desc provides a summary comparing the original data to cleaned
@IN nypl_menus_2  @URI directory:nypl_menus_2/
@OUT diff_summary  @URI file:diff_summary.png/
@OUT clean_usecase_query @URI file:clean_usecase_query.csv
"""
"""@END compare_updates"""
"""@END project_workflow"""