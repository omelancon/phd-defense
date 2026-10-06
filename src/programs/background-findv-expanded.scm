(define (findv v pred)
  (let loop ((i 0))
    (cond
      ((>= i (if #|@vec-check|#(vector? v)#|@end|# (##vector-length v)
                             (fail)))
       #f)
      ((pred v i) i)
      (else (loop (cond (#|@fix-check|#(fixnum? i)#|@end|#
                         (or #|@ovf-check|#(fx+? i 1)#|@end|# (##+ i 1)))
                        (#|@flo-check|#(flonum? i)#|@end|# (fl+ i 1.0))
                        (else (##+ i 1))))))))

(let ((arg (findv v odd?)))
  (if (and #|@ref-vec|#(vector? v)#|@end|# #|@ref-fix|#(fixnum? arg)#|@end|#
           #|@ref-lo|#(fx>= arg 0)#|@end|# #|@ref-hi|#(fx< arg (##vector-length v))#|@end|#)
      (##vector-ref v arg) (fail)))