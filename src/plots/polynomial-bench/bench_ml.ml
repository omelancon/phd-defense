let[@inline never] p x = x * x + x
let () =
  let n = int_of_string Sys.argv.(1) in
  let acc = ref 0 in
  for i = 0 to n - 1 do acc := !acc + p (i land 1023) done;
  print_int !acc; print_newline ()
