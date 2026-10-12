(define (vector-safe-ref v i)
  (if (and (fixnum? i)
           #|@src-lo|#(>= i 0)#|@end|#
           #|@src-hi|#(< i (if (vector? v) (##vector-length v) (fail)))#|@end|#)
      (if (and (vector? v)
               (fixnum? i)
               #|@ref-lo|#(fx>= i 0)#|@end|#
               #|@ref-hi|#(fx< i (##vector-length v))#|@end|#)
          (##vector-ref v i)
          (fail))
      #f))

(vector-safe-ref #(1 2 3) (read))
