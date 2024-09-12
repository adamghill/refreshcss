# ruff: noqa


def parse(css_text: str, html_classes: set[str], html_ids: set[str]) -> str:
    #     # https://gist.github.com/erikrose/5624176

    #     from parsimonious.grammar import Grammar

    #     grammar = Grammar(
    #         r"""
    #     program = S* stylesheet
    #     digit = ~"[0123456789]"
    #     nmstart = ~"[ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_]"
    #     nmchar = nmstart / ~"[0123456789-]"
    #     minus = "-"
    #     IDENT = nmstart nmchar*
    #     NUMBER = digit+ / (digit* "." digit+)
    #     ws = ~r"[ \t]"
    #     nl = ~r"[\n]"
    #     comment = "/*" (!"*/" ~".")* "*/"
    #     ws_or_nl = ws / nl
    #     S = ws_or_nl / comment
    #     stylesheet = stmt*
    #     stmt = rule / media
    #     rule = rule_lhs rule_rhs
    #     rule_lhs = selector more_selector*
    #     more_selector =  "," S* selector
    #     rule_rhs = "{" decls  ";"? S* "}" S*
    #     decls = S* declaration more_declaration*
    #     more_declaration = ";" S* declaration
    #     selector = simple_selector selector_trailer?
    #     selector_trailer = selector_trailer_a / selector_trailer_b / selector_trailer_c / selector_trailer_d
    #     selector_trailer_a = combinator selector
    #     selector_trailer_b = S+ combinator selector
    #     selector_trailer_c = S+ selector
    #     selector_trailer_d = S+
    #     simple_selector = (element_name simple_selector_etc*) / (simple_selector_etc+)
    #     simple_selector_etc = id_selector / class_selector / attrib_selector / pseudo_selector
    #     element_name = element_selector / wild_element_selector
    #     element_selector = IDENT
    #     wild_element_selector = "*"
    #     id_selector     = "#" IDENT
    #     class_selector  = "." IDENT
    #     attrib_selector = "[" S* IDENT ( ("=" / "~=" / "|=" ) S* ( IDENT / STRING ) S*)? "]"
    #     pseudo_selector = ":" IDENT
    #     tbd_pseudo_selector = ":" IDENT ( "(" ( IDENT S* )? ")" )?
    #     combinator = ("+" / ">") S*
    #     declaration = property ":" S* expr priority?
    #     property = IDENT S*
    #     priority = "!" S*
    #     expr = term ( operator? term )*
    #     operator = operator_a S*
    #     operator_a =  "/" / ","
    #     term = (unary_op measure) / measure / other_term
    #     unary_op = "-" / "+"
    #     measure = mess S*
    #     mess = em_m / ex_m / px_m / cm_m / mm_m / in_m / pt_m / pc_m / deg_m / rad_m / grad_m / ms_m / s_m / hx_m / khz_m / percent_m / dim_m / raw_m
    #     em_m = NUMBER "em"
    #     ex_m = NUMBER "ex"
    #     px_m = NUMBER "px"
    #     cm_m = NUMBER "cm"
    #     mm_m = NUMBER "mm"
    #     in_m = NUMBER "in"
    #     pt_m = NUMBER "pt"
    #     pc_m = NUMBER "pc"
    #     deg_m = NUMBER "deg"
    #     rad_m = NUMBER "rad"
    #     grad_m = NUMBER "grad"
    #     ms_m = NUMBER "ms"
    #     s_m = NUMBER "s"
    #     hx_m = NUMBER "hz"
    #     khz_m = NUMBER "khz"
    #     percent_m = NUMBER "%"
    #     dim_m = NUMBER IDENT
    #     raw_m = NUMBER
    #     other_term = (STRING S*) / (URI S*) / (IDENT S*) / (hexcolor S*) / function
    #     function = IDENT "(" S* expr ")" S*
    #     STRING = '"' ( !'"' ~"." )* '"'
    #     URI = "url(" ( !")" ~"." )* ")"
    #     hexcolor = ("#" hex hex hex hex hex hex) / ("#" hex hex hex)
    #     hex = ~r"[0123456789abcdefABCDEF]"
    #     medium = IDENT S*
    #     medium_list = medium ("," S* medium)*
    #     media = "@media" S* medium "{" S* stylesheet "}"
    #     """
    #     )

    #     p = grammar.parse(".container { color: blue; }")
    #     print("p", p)

    #     assert 0
    pass
