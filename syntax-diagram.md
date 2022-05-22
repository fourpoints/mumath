"""
Math    ::= Table | Inline
Table   ::= Row*
Row     ::= Inline*
Inline  ::= NoTag | Block
Block   ::= Expr (BlockOp Expr)*
Expr    ::= UnOp? Expr (BinOp Expr)*
"""
