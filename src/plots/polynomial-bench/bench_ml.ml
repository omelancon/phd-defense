let[@inline never] p x = x * x + x
let () =
  Scanf.scanf " %d %d" (fun n x ->
    let acc = ref 0 in
    for _ = 1 to n do acc := !acc + p x done;
    print_int !acc; print_newline ())
