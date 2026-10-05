(define (findv v pred)
  (if #|@lifted|#(vector? v)#|@end|#
      (let loop ((i 0))
        (cond
          (#|@fx-gte|#(fx>= i (##vector-length v))#|@end|# #f)
          ((pred v i) i)
          (else (loop #|@fx-add|#(fx+ i 1)#|@end|#))))
      (fail)))

(let ((arg (findv v odd?)))
  (if #|@ref-fix|#(fixnum? arg)#|@end|#
      #|@vref|#(##vector-ref v arg)#|@end|#
      (fail)))