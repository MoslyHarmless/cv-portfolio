import{A as e,Kt as t,T as n,X as r,a as i,c as a,cn as o,i as s,k as c,q as l,qt as u}from"./three-core-wnWK4b0n.js";import{t as d}from"./three-renderer-CrXmNnlV.js";function f(f){let p=f.closest(`.hero`),m=new d({alpha:!0,antialias:!1,powerPreference:`low-power`});m.setPixelRatio(Math.min(window.devicePixelRatio||1,2)),m.setClearColor(657936,0),m.domElement.setAttribute(`aria-hidden`,`true`),m.domElement.setAttribute(`role`,`presentation`),f.append(m.domElement);let h=new t,g=new l(42,1,.1,30);g.position.z=9;let _=new n;h.add(_);let v=window.innerWidth<1100?2800:4800,y=new Float32Array(v*3),b=new Float32Array(v*3),x=new Float32Array(v),S=new a(`#af83ff`),C=new a(`#71d4ec`),w=new a,T=Math.PI*(3-Math.sqrt(5));for(let e=0;e<v;e++){let t=1-e/(v-1)*2,n=Math.sqrt(1-t*t),r=T*e,i=1.88+Math.sin(r*4+t*8)*.045;y[e*3]=Math.cos(r)*n*i,y[e*3+1]=t*i,y[e*3+2]=Math.sin(r)*n*i,w.copy(S).lerp(C,Math.max(0,(Math.cos(r)+t+.2)*.36)),w.toArray(b,e*3),x[e]=1.1+e*13%17/13}let E=new i;E.setAttribute(`position`,new s(y,3)),E.setAttribute(`aColor`,new s(b,3)),E.setAttribute(`aSize`,new s(x,1));let D=new u({uniforms:{uTime:{value:0},uDpr:{value:m.getPixelRatio()},uPointer:{value:new o(0,0,2)},uStrength:{value:0}},vertexShader:`
      uniform float uTime;
      uniform float uDpr;
      uniform vec3 uPointer;
      uniform float uStrength;
      attribute vec3 aColor;
      attribute float aSize;
      varying vec3 vColor;
      varying float vOpacity;
      void main() {
        vec3 point = position;
        float wave = sin(point.y * 3.0 + uTime * 0.65) * sin(point.x * 2.6 - uTime * 0.4);
        point += normalize(point) * wave * 0.07;
        vec3 delta = uPointer - point;
        point += delta * exp(-dot(delta, delta) * 1.2) * uStrength * 0.16;
        vec4 viewPosition = modelViewMatrix * vec4(point, 1.0);
        gl_Position = projectionMatrix * viewPosition;
        gl_PointSize = aSize * uDpr * (8.0 / -viewPosition.z);
        vColor = aColor;
        vOpacity = 0.25 + smoothstep(-1.9, 1.9, point.z) * 0.65;
      }
    `,fragmentShader:`
      varying vec3 vColor;
      varying float vOpacity;
      void main() {
        float radius = length(gl_PointCoord - vec2(0.5));
        if (radius > 0.5) discard;
        float alpha = smoothstep(0.5, 0.05, radius) * vOpacity;
        gl_FragColor = vec4(vColor, alpha);
        #include <colorspace_fragment>
      }
    `,transparent:!0,depthWrite:!1,blending:2});_.add(new r(E,D));let O=[];for(let t=0;t<3;t++){let n=[];for(let e=0;e<180;e++){let r=e/180*Math.PI*2;n.push(new o(Math.cos(r)*(2.06+t*.11),Math.sin(r)*(2.06+t*.11),0))}let r=new i().setFromPoints(n),a=new c({color:t===2?`#78ccdd`:`#b18aef`,transparent:!0,opacity:t===1?.17:.3,depthWrite:!1,blending:2}),s=new e(r,a);s.rotation.set(.85+t*.28,t*.65,-.4+t*.6),_.add(s),O.push(s)}let k=1,A=1,j=1,M=1,N=0,P=0,F=0,I=!0,L=!1,R=!1,z=0,B=0,V=0,H=0,U=0,W=new o(0,0,2);function G(){k=f.clientWidth,A=f.clientHeight,(k!==H||A!==U)&&(H=k,U=A,m.setPixelRatio(Math.min(window.devicePixelRatio||1,2)),m.setSize(k,A,!1),D.uniforms.uDpr.value=m.getPixelRatio(),g.aspect=k/Math.max(A,1),g.updateProjectionMatrix(),M=2*Math.tan(42*Math.PI/360)*g.position.z,j=M*g.aspect,_.position.set(j*.255,.02,0),_.scale.setScalar(k<1100?.83:1))}function K(e){if(e.pointerType===`touch`)return;let t=p.getBoundingClientRect();N=(e.clientX-t.left)/k-.5,P=(e.clientY-t.top)/A-.5,W.set(N*j-_.position.x,-P*M,1.7),F=1}function q(){F=0,N=0,P=0}function J(e){if(z=0,R||document.hidden||!I||L)return;let t=Math.min((e-(B||e))/1e3,.05);B=e,V+=t;let n=1-Math.exp(-t*4);D.uniforms.uTime.value=V,D.uniforms.uPointer.value.lerp(W,n),D.uniforms.uStrength.value+=(F-D.uniforms.uStrength.value)*n,_.rotation.y+=(V*.025+N*.18-_.rotation.y)*n,_.rotation.x+=(P*.1-.15-_.rotation.x)*n,_.rotation.z=-.12,m.render(h,g),z=requestAnimationFrame(J)}function Y(){cancelAnimationFrame(z),z=0,B=0,!R&&!document.hidden&&I&&!L&&(z=requestAnimationFrame(J))}function X(e){e.preventDefault(),L=!0,document.documentElement.classList.remove(`has-webgl`),Y()}function Z(){L=!1,document.documentElement.classList.add(`has-webgl`),Y()}G();let Q=new ResizeObserver(G);Q.observe(f);let $=new IntersectionObserver(([e])=>{I=e.isIntersecting,Y()});return $.observe(p),p.addEventListener(`pointermove`,K,{passive:!0}),p.addEventListener(`pointerleave`,q),document.addEventListener(`visibilitychange`,Y),m.domElement.addEventListener(`webglcontextlost`,X),m.domElement.addEventListener(`webglcontextrestored`,Z),m.render(h,g),document.documentElement.classList.add(`has-webgl`),Y(),()=>{R=!0,cancelAnimationFrame(z),Q.disconnect(),$.disconnect(),p.removeEventListener(`pointermove`,K),p.removeEventListener(`pointerleave`,q),document.removeEventListener(`visibilitychange`,Y),m.domElement.removeEventListener(`webglcontextlost`,X),m.domElement.removeEventListener(`webglcontextrestored`,Z),E.dispose(),D.dispose(),O.forEach(e=>{e.geometry.dispose(),e.material.dispose()}),m.dispose(),m.forceContextLoss(),m.domElement.remove(),document.documentElement.classList.remove(`has-webgl`)}}export{f as initHero3D};