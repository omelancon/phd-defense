(define (findv v pred)
  (let loop ((i 0))
    (cond
      ((fx>= i (if #|@vec-check|#(vector? v)#|@end|# (##vector-length v)
                               (fail)))
       #f)
      ((pred v i) i)
      (else (loop (fx+ i 1))))))

(let ((arg (findv v odd?)))
  (if (and #|@ref-fix|#(fixnum? arg)#|@end|#
           #|@bound-check|#(fx>= arg 0) (fx< arg (##vector-length v))#|@end|#)
      (##vector-ref v arg) (fail)))