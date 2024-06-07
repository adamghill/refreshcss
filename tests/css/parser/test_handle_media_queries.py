# from refreshcss.css.regex_parser import _handle_media_queries


# def test_handle_media_queries():
#     expected = """
#   .is-visibility-hidden-fullhd,
#   .is-invisible-fullhd {
#     visibility: hidden !important;
#   }
# """

#     css_rule = """@media screen and (min-width: 1408px) {
#   .is-visibility-hidden-fullhd,
#   .is-invisible-fullhd {
#     visibility: hidden !important;
#   }
# }
# """

#     actual = _handle_media_queries(css_rule)

#     assert expected == actual
