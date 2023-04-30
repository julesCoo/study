mod geodesy;

fn main() {
    let w1 = geodesy::angle::dms(124.0, 30.0, 30.0);

    // Print out w1 as radians
    println!("w1 as radians: {}", w1.to_());
}
