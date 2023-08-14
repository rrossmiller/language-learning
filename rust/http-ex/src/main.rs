fn main() {
    label();
}

/// get the label for cetirizine
fn label() {
    let rx_cui = "1482533";
    let url = format!(
        "https://api.fda.gov/drug/label.json?search=openfda.rxcui.exact:{}",
        rx_cui
    );

    let body = reqwest::blocking::get(url).unwrap().text().unwrap();
    println!("{:?}", body);
}
