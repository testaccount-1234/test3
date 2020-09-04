counter=1
dmin=10
dmax=15
dskip=5
order_of_tensor=3


for ((legdim=dmin; legdim<=dmax; legdim+=dskip)); do
    batchsize=$((legdim**2))
    H=1
    mmin=$((batchsize*order_of_tensor*H+batchsize))
    mmax=$((order_of_tensor**legdim+batchsize))
    mskip=$((batchsize*order_of_tensor))
    if ($((10*mskip)) -lt $((mmax-mmin))); then
        mskip=$(((mmax-mmin)/(10*mskip)))
        echo 'if'
    fi
    echo $legdim
    echo $mmin
    echo $mmax
    echo $mskip
    for ((meas=mmin; meas<=mmax; meas+=mskip)); do
        echo "python recover_theta.py \"{'measurements': $meas, 'order': '$order_of_tensor','leg_dimension': '$legdim','file_name': 'legdim=${legdim}_meas=${meas}', 'batchsize': ${batchsize} ,'minimal_l2loss': '0.00000001', 'minimal_step_size': '0.00000001'}\"" > job_rec_$counter.sh
        ((counter++))
    done
done

