gadmin config set GSQL.UDF.EnablePutExpr true &&
  gadmin set GSQL.UDF.Policy.Enable false &&
  gadmin config apply &&
  gadmin restart gsql

pass=

gsql -u user_1 -p "$pass" PUT ExprFunctions FROM "/home/tigergraph/ExprFunctions.hpp"
