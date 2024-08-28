// Copyright Materialize, Inc. and contributors. All rights reserved.
//
// Use of this software is governed by the Business Source License
// included in the LICENSE file.
//
// As of the Change Date specified in that file, in accordance with
// the Business Source License, use of this software will be governed
// by the Apache License, Version 2.0.

// use crate::JoinInput::{Complex, GlobalId};

pub static SDH_LOGGER: std::sync::atomic::AtomicBool = std::sync::atomic::AtomicBool::new(false);

#[macro_export]
macro_rules! mzdbg {
    ($($args:tt)*) => {
        if workspace_hack::SDH_LOGGER.load(std::sync::atomic::Ordering::Acquire) {
            eprintln!("\nsdh [{}:{}] {}", file!(), line!(), format!($($args)*));
        }
    };
}

// enum JoinOrigin {
//     // "the reason for the join to exist"
//     InnerJoin(SqlConcept),
//     FusedInnerJoin(FusedInnerJoin),
//     OuterJoinPart(OuterJoinPart, SqlConcept),
// }
//
// #[derive(Clone)]
// enum SqlConcept {
//     InnerJoin {
//         input0: JoinInput,
//         input1: JoinInput,
//     }, // Either a `FROM` clause's implicit joining, or `INNER JOIN` or `CROSS JOIN`  todo: split these?
//     OuterJoin(OuterJoin),
// }
//
// struct FusedInnerJoin {
//     // todo: fusion between different join kinds? Maybe just modify to JoinFusion, and have `origin: Vec<JoinOrigin>`. And print simply as "FusedJoin t1, t2, t3".
//     inputs: Vec<JoinInput>,
//     origin: JoinOrigin, // shown only in verbose mode // todo: sometimes our JoinOrigin struct can't encompass each of the joins that were fused, e.g., if in different ctes. Maybe Vec<JoinOrigin>? (Or if we want to make it fancy later, then `Map<JoinOrigin, Set<index>>`, where index is a number pointing to `inputs`.)
// }
//
// #[derive(Clone)]
// struct OuterJoin {
//     input0: JoinInput, // SQL-level input
//     input1: JoinInput, // SQL-level input
//     kind: JoinKind,    // Left/Right/Full
// }
//
// #[derive(Clone)]
// pub enum JoinKind {
//     LeftOuter,
//     RightOuter,
//     FullOuter,
// }
//
// enum OuterJoinPart {
//     Inner,
//     Semi,
//     VojFinishing,
//     InnerPartDistinctKeys, // on Reduce
// }
//
// enum MirArrangeBy {
//     JoinInput(JoinOrigin, usize),
// }
//
// #[derive(Clone)]
// enum JoinInput {
//     // Important: SQL-level
//     GlobalId(usize),
//     Complex(SqlConcept), // todo
// }
//
// struct Subquery {
//     // todo
// }
//
// fn create() {
//     let t1 = 1;
//     let t2 = 2;
//     let t3 = 3;
//
//     let j1 = JoinOrigin::FusedInnerJoin(FusedInnerJoin {
//         inputs: vec![
//             JoinInput::GlobalId(1),
//             JoinInput::GlobalId(2),
//             JoinInput::GlobalId(3),
//         ],
//         origin: JoinOrigin::InnerJoin(SqlConcept::InnerJoin {
//             input0: JoinInput::Complex(SqlConcept::InnerJoin {
//                 input0: JoinInput::GlobalId(t1),
//                 input1: JoinInput::GlobalId(t2),
//             }),
//             input1: JoinInput::GlobalId(t3),
//         }),
//     });
//
//     let j2 = JoinOrigin::FusedInnerJoin(FusedInnerJoin {
//         inputs: vec![
//             JoinInput::GlobalId(t1),
//             JoinInput::GlobalId(t2),
//             JoinInput::GlobalId(t3),
//         ],
//         origin: JoinOrigin::InnerJoin(SqlConcept::InnerJoin {
//             input0: JoinInput::Complex(SqlConcept::InnerJoin {
//                 input0: JoinInput::GlobalId(t1),
//                 input1: JoinInput::GlobalId(t2),
//             }),
//             input1: JoinInput::GlobalId(t3),
//         }),
//     });
//
//     let q3common = SqlConcept::InnerJoin {
//         input0: GlobalId(t1),
//         input1: GlobalId(t2),
//     };
//     let subq1 = JoinOrigin::InnerJoin(q3common.clone());
//     let j3 = JoinOrigin::InnerJoin(SqlConcept::InnerJoin {
//         input0: Complex(q3common),
//         input1: GlobalId(t3),
//     });
//
//     let q4common1 = SqlConcept::OuterJoin(OuterJoin {
//         input0: JoinInput::GlobalId(t1),
//         input1: JoinInput::GlobalId(t2),
//         kind: JoinKind::LeftOuter,
//     });
//     let q4inner1 = JoinOrigin::OuterJoinPart(OuterJoinPart::Inner, q4common1.clone());
//     let q4semijoin1 = JoinOrigin::OuterJoinPart(OuterJoinPart::Semi, q4common1.clone());
//     let q4common2 = SqlConcept::OuterJoin(OuterJoin {
//         input0: JoinInput::Complex(q4common1),
//         input1: JoinInput::GlobalId(t3),
//         kind: JoinKind::LeftOuter,
//     });
//     let q4inner2 = JoinOrigin::OuterJoinPart(OuterJoinPart::Inner, q4common2.clone());
//     let q4semijoin2 = JoinOrigin::OuterJoinPart(OuterJoinPart::Semi, q4common2);
//
//     println!("{j1:?} {j2:?} {j1:?} {j1:?} {j1:?} {j1:?} {j1:?}");
// }
