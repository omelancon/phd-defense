(define (p x)
  (let ((y (cond (#|@x-fix|#(fixnum? x)#|@end|#
                  (or #|@x-ovf|#(fx*? x x)#|@end|#
                      (##* x x)))
                 (#|@x-flo|#(flonum? x)#|@end|# (fl* x x))
                 (else (##* x x)))))
    (cond (#|@y-fix|#(and (fixnum? y) (fixnum? x))#|@end|#
           (or #|@y-ovf|#(fx+? y x)#|@end|#
               (##+ y x)))
          (#|@y-flo|#(and (flonum? y) (flonum? x))#|@end|#
           (fl+ y x))
          (else (##+ y x)))))