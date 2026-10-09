let f (type a) (module N : NUM with type t = a) (x : a) =
  N.add (N.mul x x) x

let _ = f (module Int) 5        (* 30 *)
let _ = f (module Float) 3.14    (* ~12.9996 *)