(define (vector-safe-ref v i)
  (if (and (fixnum? i) (>= i 0) (< i (vector-length v)))
      (vector-ref v i)
      #f))

(vector-safe-ref #(1 2 3) (read))
