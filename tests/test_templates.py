from templates.tmanager import TManager

def test_dialog_logon_template_renders():
    tm = TManager()
    context = {
        "ALGDATE": "20250320",
        "ALGTIME": "125232",
        "ALGUSER": "DDIC",
        "ALGCLIENT": "800",
        "ALGTEXT": "Login successful",
        "PARAM1": "B",
        "PARAM3": "A",
        "ALGSYSTEM": "w16s24id8606"
    }
    output = tm.render_template("dialog_logon/base_template.txt", context)
    assert "DDIC" in output
    assert "Login successful" in output
