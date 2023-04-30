use crate::geodesy::vv::F64v;

use std::f64::consts::PI;

pub struct Angle {
    radians: F64v,
}

/* Constructors */

pub fn radians(value: F64v) -> Angle {
    Angle { radians: value }
}

pub fn degrees(value: F64v) -> Angle {
    Angle {
        radians: F64v {
            value: value.value * PI / 180.0,
            variance: value.variance * PI / 180.0,
        },
    }
}

pub fn gradians(value: F64v) -> Angle {
    Angle {
        radians: F64v {
            value: value.value * PI / 200.0,
            variance: value.variance * PI / 200.0,
        },
    }
}

pub fn dms(degrees: F64v, minutes: F64v, seconds: F64v) -> Angle {
    let value = degrees.value + minutes.value / 60.0 + seconds.value / 3600.0;
    let variance = degrees.variance + minutes.variance / 60.0 + seconds.variance / 3600.0;
    Angle {
        radians: F64v {
            value: value * PI / 180.0,
            variance: variance * PI / 180.0,
        },
    }
}

pub fn gms(gradians: F64v, minutes: F64v, seconds: F64v) -> Angle {
    let value = gradians.value + minutes.value / 100.0 + seconds.value / 10000.0;
    let variance = gradians.variance + minutes.variance / 100.0 + seconds.variance / 10000.0;
    Angle {
        radians: F64v {
            value: value * PI / 200.0,
            variance: variance * PI / 200.0,
        },
    }
}

/* Converters */

impl Angle {
    pub fn to_radians(angle: Angle) -> F64v {
        angle.radians
    }

    pub fn to_degrees(angle: Angle) -> F64v {
        F64v {
            value: angle.radians.value * 180.0 / PI,
            variance: angle.radians.variance * 180.0 / PI,
        }
    }

    pub fn to_gradians(angle: Angle) -> F64v {
        F64v {
            value: angle.radians.value * 200.0 / PI,
            variance: angle.radians.variance * 200.0 / PI,
        }
    }

    pub fn to_dms(angle: Angle) -> (F64v, F64v, F64v) {
        let degrees = angle.radians.value * 180.0 / PI;
        let minutes = (degrees - degrees.trunc()) * 60.0;
        let seconds = (minutes - minutes.trunc()) * 60.0;
        (
            F64v {
                value: degrees,
                variance: angle.radians.variance * 180.0 / PI,
            },
            F64v {
                value: minutes,
                variance: angle.radians.variance * 180.0 / PI,
            },
            F64v {
                value: seconds,
                variance: angle.radians.variance * 180.0 / PI,
            },
        )
    }

    pub fn to_gms(angle: Angle) -> (F64v, F64v, F64v) {
        let gradians = angle.radians.value * 200.0 / PI;
        let minutes = (gradians - gradians.trunc()) * 100.0;
        let seconds = (minutes - minutes.trunc()) * 100.0;
        (
            F64v {
                value: gradians,
                variance: angle.radians.variance * 200.0 / PI,
            },
            F64v {
                value: minutes,
                variance: angle.radians.variance * 200.0 / PI,
            },
            F64v {
                value: seconds,
                variance: angle.radians.variance * 200.0 / PI,
            },
        )
    }
}
