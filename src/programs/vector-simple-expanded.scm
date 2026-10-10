(let ((i (read))
      (v #(1 2 3)))
  (if (and
        (fixnum? i)
        (fx< i
             (if (vector? v)
                 (##vector-length v)
                 (fail))))
      (if (and
            (vector? v)
            (fixnum? i)
            (fx>= i 0)
            #|@ref-hi|#(fx< i (##vector-length v))#|@end|#)
          (##vector-ref v i)
          (fail))
      #f))
