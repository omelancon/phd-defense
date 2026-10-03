(define (sum-to-n n)
  (let loop ((i 1) (sum 0))
    (if (> i n)
        sum
        (loop (+ i 1) (+ sum i)))))

(let ((index (sum-to-n 3)))
  (display (if (and #|@int-check|# (integer? index) #|@end|#
                    #|@nonneg-check|# (>= index 0) #|@end|#
                    (< index (vector-length v)))
               (##vector-ref v index)
               (fail))))
