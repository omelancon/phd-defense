let f x = x * x + x

let _ = (f 5)  (* 30 *)
#|@error|#let _ = (f 3.14)  (* type error *)#|@end|#