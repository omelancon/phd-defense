(define (findv v pred)
  (let loop ((i 0))
    (cond
      ((>= i (vector-length v)) #f)
      ((pred v i) i)
      (else (loop (+ i 1))))))

(vector-ref v (findv v odd?))