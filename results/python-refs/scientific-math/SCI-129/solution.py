import sys
from itertools import combinations

def circumcenter(p1,p2,p3):
    ax,ay=p1; bx,by=p2; cx,cy=p3
    d=2*(ax*(by-cy)+bx*(cy-ay)+cx*(ay-by))
    if abs(d)<1e-12: return None
    ux=((ax*ax+ay*ay)*(by-cy)+(bx*bx+by*by)*(cy-ay)+(cx*cx+cy*cy)*(ay-by))/d
    uy=((ax*ax+ay*ay)*(cx-bx)+(bx*bx+by*by)*(ax-cx)+(cx*cx+cy*cy)*(bx-ax))/d
    return (ux,uy)

def clip_segment(x1,y1,x2,y2,xmin,ymin,xmax,ymax):
    # Liang-Barsky
    dx=x2-x1; dy=y2-y1
    p=[-dx,dx,-dy,dy]
    q=[x1-xmin,xmax-x1,y1-ymin,ymax-y1]
    u1=0.0; u2=1.0
    for i in range(4):
        if abs(p[i])<1e-12:
            if q[i]<0: return None
        else:
            t=q[i]/p[i]
            if p[i]<0:
                if t>u2: return None
                if t>u1: u1=t
            else:
                if t<u1: return None
                if t<u2: u2=t
    nx1=x1+u1*dx; ny1=y1+u1*dy
    nx2=x1+u2*dx; ny2=y1+u2*dy
    return (nx1,ny1,nx2,ny2)

def perp_bisector_segment(p1,p2,xmin,ymin,xmax,ymax):
    # Line equidistant from p1,p2: midpoint, direction perpendicular to p2-p1
    mx=(p1[0]+p2[0])/2; my=(p1[1]+p2[1])/2
    dx=p2[0]-p1[0]; dy=p2[1]-p1[1]
    # perpendicular dir: (-dy, dx)
    px=-dy; py=dx
    # Take large segment
    L=1e6
    x1=mx-L*px; y1=my-L*py
    x2=mx+L*px; y2=my+L*py
    return clip_segment(x1,y1,x2,y2,xmin,ymin,xmax,ymax)

def main():
    data=sys.stdin.read().split()
    if not data:
        print('Num edges: 0'); return
    idx=0
    n=int(data[idx]); idx+=1
    pts=[]
    for _ in range(n):
        x=float(data[idx]); y=float(data[idx+1]); idx+=2
        pts.append((x,y))
    # Bounding box: min/max of points expanded by 5
    if n==0:
        print('Num edges: 0'); return
    xs=[p[0] for p in pts]; ys=[p[1] for p in pts]
    xmin=min(xs)-5; xmax=max(xs)+5
    ymin=min(ys)-5; ymax=max(ys)+5
    
    # Naive Voronoi: for each pair, compute perp bisector segment clipped to box,
    # then for each point on the segment check if it's closest to those two sites
    # (or equidistant) and no other site is closer.
    edges=[]
    for i,j in combinations(range(n),2):
        seg=perp_bisector_segment(pts[i],pts[j],xmin,ymin,xmax,ymax)
        if seg is None: continue
        x1,y1,x2,y2=seg
        # Sample along segment, find subsegment where pts[i],pts[j] are tied for closest
        # Use parametric t in [0,1], find intervals
        # For each other point k, find where dist to k < dist to i (equivalently to j)
        # dist^2 to i along segment is quadratic in t, same for k
        # We want: for all k != i,j: dist(t,k)^2 >= dist(t,i)^2
        # i.e. dist(t,k)^2 - dist(t,i)^2 >= 0
        # This is linear in t (quadratics cancel)
        # f_k(t) = (x(t)-kx)^2+(y(t)-ky)^2 - (x(t)-ix)^2-(y(t)-iy)^2
        #       = -2*x(t)*(kx-ix) -2*y(t)*(ky-iy) + (kx^2+ky^2-ix^2-iy^2)
        # x(t)=x1+t*(x2-x1), y(t)=y1+t*(y2-y1)
        # f_k(t) = A + B*t where
        ix,iy=pts[i]
        lo=0.0; hi=1.0
        valid=True
        for k in range(n):
            if k==i or k==j: continue
            kx,ky=pts[k]
            # A = -2*x1*(kx-ix) -2*y1*(ky-iy) + (kx*kx+ky*ky-ix*ix-iy*iy)
            # B = -2*(x2-x1)*(kx-ix) -2*(y2-y1)*(ky-iy)
            A=-2*x1*(kx-ix)-2*y1*(ky-iy)+(kx*kx+ky*ky-ix*ix-iy*iy)
            B=-2*(x2-x1)*(kx-ix)-2*(y2-y1)*(ky-iy)
            # Need A+B*t >= 0 for t in [lo,hi]
            if abs(B)<1e-12:
                if A<-1e-9: valid=False; break
            else:
                t0=-A/B
                if B>0:
                    if t0>lo: lo=t0
                else:
                    if t0<hi: hi=t0
                if lo>hi+1e-9: valid=False; break
        if not valid: continue
        if hi-lo<1e-9: continue
        nx1=x1+lo*(x2-x1); ny1=y1+lo*(y2-y1)
        nx2=x1+hi*(x2-x1); ny2=y1+hi*(y2-y1)
        edges.append((nx1,ny1,nx2,ny2))
    
    # Sort edges for determinism
    def fmt(v): return f'{v:.4f}'
    out=[]
    for e in edges:
        x1,y1,x2,y2=e
        # Normalize endpoint order
        if (x1,y1)>(x2,y2):
            x1,y1,x2,y2=x2,y2,x1,y1
        out.append((x1,y1,x2,y2))
    out.sort()
    for x1,y1,x2,y2 in out:
        print(f'({fmt(x1)},{fmt(y1)})-({fmt(x2)},{fmt(y2)})')
    print(f'Num edges: {len(out)}')

main()
