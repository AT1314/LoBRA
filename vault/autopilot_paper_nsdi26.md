---
title: "autopilot_paper_nsdi26"
date: "2025-09-17"
source: "inbox/autopilot_paper_nsdi26.pdf"
format: "PDF Document"
pages: "27"
converted: "2025-10-31 10:24:37"
---

# autopilot_paper_nsdi26

**Pages:** 27


## Page 1

Pilot Execution: Simulating Failure Recovery In Situ for
Production Distributed Systems
Submission # XXX
Abstract
Modern distributed systems depend on failure recovery to
ensure availability and correctness in the face of faults–yet
ironically, it is the recovery itself that often triggers the most
severe and irreversible failures. Our study on 75 real-world
recovery failures shows that the challenges primarily come
from complex cross-system and cross-component interactions.
To enable safe and predictable failure recovery, we introduce
PILOT , a new execution model that enables dry-run simu-
lations of recovery actions within production systems. By
allowing operators to observe the effects of recovery actions
before applying them, it reduces the risk of cascading failures
and unintended side effects. We implement PILOT in five
large-scale systems and demonstrate that it can automatically
uncover nine out of ten severe recovery failures without intro-
ducing noticeable additional unavailability. It also exposes a
unknown recovery bug in the latest version of HBase.
1 Introduction
Cloud failures pose a critical challenge to the reliability of
modern digital infrastructure, where even brief disruptions
can lead to substantial financial and operational losses. When
failures occur, recovery mechanisms are crucial to minimiz-
ing impact. Modern cloud systems employ various recovery
strategies. Clients redirect failed requests to replicas when pri-
mary nodes fail, systems replicate data to ensure availability,
and auto-scaling adjusts resources to handle increased load.
These recovery processes may be triggered automatically by
monitoring tools or manually by operators.
Unfortunately, incorrect failure recovery itself has been a
major source of catastrophic incidents [ 58, 89, 99]. When
recovery is triggered, the system is usually already in a fragile
and vulnerable state. It is also known that recovery logic is
often under-tested and more error-prone than other system
components, largely because of the complexity of writing and
exercising comprehensive tests for recovery paths [57]. The
complicated interactions in cloud systems make anticipating
the action impact particularly challenging. Consequently, re-
covery actions are often ineffective, or even amplify failures
instead, turning a minor fault into cluster-wide disaster.
For example, in one production incident [ 12] in HBasechange
lead-
ing
sen-
tence
clusters (Figure 1), when one region server attempts to read
a write-ahead-log file, it crashes as the file was corrupted.
HBase tries to recover the issue by transferring the workloads
on that server to other servers, however, the remaining servers
also experience the same issue and crash since the underlying
file issue has not been resolved. Unless manually stopped, this
loop will continue and eventually bring down all servers in the
cluster. Such issues cannot be simply tolerated by traditional
redundancy and replication techniques [63].
Many real-world evidence [44, 48, 59, 88, 93, 94] show that
recovery failures are severe problems. In one incident [96],
Microsoft activated DDoS protection mechanisms–such as
traffic filtering and rate limiting via Azure services–to mit-
igate a massive cyberattack flooding its systems. However,
a misconfiguration in these defenses inadvertently amplified
the attack’s effects, extending the outage to nearly 10 hours
and disrupting services like Microsoft 365 worldwide.
Thus, there is a critical need for a paradigm shift from
executing unvalidated, potentially hazardous recovery actions
to systematically validating recovery strategies before deploy-
ment. One promising direction involves verifying planned
changes in distributed systems through behavior testing on
abstract models [46, 49, 55]. However, these models often
fail to capture low-level implementation issues, limiting their
effectiveness in exposing subtle but critical faults. Moreover,
abstract testing frameworks are typically too coarse-grained
to efficiently identify the increasingly complex failure modes
present in modern systems.
In practice, developers often resort toin situ tests on produc-
tion clusters with a rolling style. A common strategy is A/B
testing [65, 68, 81, 98]—along with similar approaches like
canary and blue/green deployments—which applies recov-
ery solutions to a subset of nodes and monitors their impact.
Yet, this method provides no assurance that failures detected
in one environment will manifest similarly on other servers.
Worse, such tests can inadvertently trigger cascading failures
due to the absence of built-in safety mechanisms, escalating
to a complete cluster outage.
In this paper we ask an ambitious question: Is it possible
to expose the potential issues of intended recovery actions
before deploying? To understand the challenges of failure
recovery in distributed systems, we first conducted a study of
60 recovery-related bugs across six widely deployed systems,
including Cassandra, HBase, and Y ARN. Our analysis reveals
that recovery failures persist throughout the software lifecycle,
often lead to severe consequences, and frequently involve
complex inter-thread and inter-service interactions. Crucially,
many of these failures could have been avoided with input
adjustments, had their impact been evaluated ahead of time.
We observe that many software tools offer a --dry-run
option before applying important changes. For example, Git
lets users preview changes before committing to avoid dis-
rupting the repository. Inspired by this, we envision enabling
a “dry-run” for risk recovery in production system operations.
1

## Page 2

Conference’17, July 2017, Washington, DC, USA Submission # XXX
Such dry-run should accurately reflect the true consequences
of the recovery action, experiencing similar problems such
as exceptions, timeouts, or excessive resource utilization. In
fact, modern software systemscomplete..
chang: add a paragraph to explain the challenges
Therefore, we propose a new execution model—pilot ex-
ecution, to validate the consequences of recovery actions
before executing them in production instances (instead of
testing clusters). Different from existing works performing
a “what-if analysis” with statistical data, pilot execution con-
ducts a dry-run of proposed recovery strategies; thus it is able
to expose subtle issues deeply hidden in the implementation.
The core of this approach is a software-based sandbox design
which isolates side effects from production traffic and a con-
text propagation mechanism which captures system dynamics
to extend the scope globally. It also employs optimization
such as caching to accelerate recovery performance.
Pilot execution enables new capabilities for distributed sys-
tems to safely deploy changes. If a round of pilot execution
reveals potentially harmful effects (e.g., writes that would cor-
rupt replicated state), the system can take preemptive action
— e.g., pausing the recovery and alerting operators. chang:
pausing the recovery process may sound concerning to some
readers, need to rephrase It also allows the system to revise or
optimize their recovery strategies and experiment with them
before applying.
Inspired by our study findings, we design and implement
PILOT , a new framework that enables pilot execution for ex-
isting distributed systems automatically. PILOT comprises a
static analysis engine and a runtime library. It identifies recov-
ery entry points through static analysis, convert recovery-
related logic to a special version compatible to phantom
thread abstraction, and instruments the code to redirect ex-
ecution to the new simulation path in parallel with the live
system. To ensure realism, pilot executions reuse the system’s
real state, while all interactions—including inter-thread com-
munication, file operations, and network calls—are safely
contained using multi-level sandboxing. This allowsPILOT to
surface the actual consequences of recovery decisions without
introducing risk or disrupting ongoing operations.
We recognize that, transparent failure recovery is extremely
difficult in the general case [ 76]. PILOT aims to provide a
useful tool for system operators which covers some of most
severe types of recovery failures.
chang: we will need to append a few more paragraphs here
to explain the usage of this tool and go through core technical
storyline
We have appliedPILOT to three production-grade systems—
Cassandra, HBase, and Y ARN—successfully uncovering nine
out of ten severe real-world recovery failures that prior testing
methods failed to expose. PILOT incurs minimal performance
overhead and enables safer, faster, and more effective recov-
ery.
Our main contributions include:
HMaster 
RegionServer coordinate 
recovery 
retry until 
all nodes down 
RegionServer 
RegionServer 
CRASH! 
CRASH! 
CRASH! 
retry 
HDFS 
Figure 1. An production incident in HBase clusters [12].
• We conduct a large-scale study of recovery failures that
identifies common patterns, consequences, and root causes.
• We design pilot execution, a new execution model which
enables dry-run simulation of recovery actions without side
effects.
• We implement real systems demonstrating PILOT ’s effec-
tiveness in exposing recovery failures with low overhead.
2 Motivation
2.1 Failure Study compact
the
de-
scrip-
tion
to
high-
light
key
ideas
Methodology We analyze eight widely deployed, large-
scale software systems spanning different functionalities and
programming languages (Table 1). To gather relevant cases,
we first extract all bug reports labeled as critical from the sys-
tems’ official issue trackers. We then filter these reports using
keywords like recovery, failover, retry, and related terms. This
process resulted in a total of 75 recovery-related failure cases.
Finding 1: Recovery failures persist throughout software
lifespan.
We found that recovery-related failures persist throughout
the software lifecycle, regardless of the system’s maturity.
Some bugs take years to expose in production, and many
others are newly introduced as the software evolves. Our
analysis shows that 38% of recovery issues occurred since
2019, showing that correct recovery remains a challenge even
for well-established systems.
Finding 2: Both automatic and manual recovery mechanisms
are prone to failures.
More than half (61%) failures happen in automatic recov-
ery mechanisms. Within automatic recovery, failures instate
recovery are the commonest (25%). This mechanism operates
on a per-node basis, reconstructing in-memory state from
durable logs, snapshots, or replicas. Kafka broker nodes illus-
trate this pattern well by replaying local logs after a crash to
restore processing state [27]. Primary-backup failover (16%)
is also frequently experiencing issues. This mechanism pro-
motes standby nodes to active status upon detecting failures,
thereby preserving availability. It is widely adopted for meta-
data nodes of distributed systems, such as the ResourceM-
anager in YARN and the NameNode in HDFS. Remaining
automatic failures happen in exception handling (13%) and
consensus-based recovery (7%). In contrast, 39% of studied
failures happen in manual recovery. For example, Cassandra
2

## Page 3

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
Software Lang. Category Version Date Sampled
HDFS Java File Sys. 2.6.1-3.4.0 2014-2024 10
HBase Java Database 0.9.0-3.0.0 2010-2025 15
Y ARN Java Resource Mgr. 2.3.0-2.9.2 2014-2025 5
TiDB Go Database 1.12.0-1.2.0 2019-2025 5
Kafka Scala Streaming 1.0.0-3.3.0 2017-2024 10
Cassandra Java Database 0.8.0-5.0.0 2011-2024 15
RabbitMQ Erlang Message Bkr. 3.6.0-3.13.6 2016-2024 5
Mesos C++ Resource Mgr. 0.21.0-1.1.2 2015-2022 10
Table 1. Sampled test datasets from eight studied systems.
administrators often use nodetool commands [ 6] to repair
data inconsistencies.
Finding 3: Recovery failures lead to severe consequences.
While many recovery failures lead toservice unavailability
(41%), they also result in other severe consequences.Resource
exhaustion (14%) is another severe result, where recovery
overloads system components, e.g., an incorrect error handler
triggers a replication storm that overwhelms the server [18].
Data loss (13%) stems from incomplete recovery that leaves
the system in an undefined state. For example, failed block
recovery prevents lease release, leaving files perpetually open
and resulting in permanent data loss [ 17]. Partial failures
(12%) such as indefinite hangs may occur when recovery fails
halfway. In one case [20], an unhandled IOException during
an RPC response in the FSEditLogAsync thread resulting in
the HDFS client thread blocked indefinitely. Performance
degradation (11%) emerges when recovery generates enor-
mous or uneven overhead. In one case, task-level recovery
ignores standby replicas once they marginally exceed a lag
threshold, triggering full state restoration on less suitable
nodes and leading to significant latency [29]. Data inconsis-
tency (9%) happens when recovery results in incorrect system
state, e.g., when stale memstore snapshots being flushed with
incorrect sequence IDs, generating HFiles misrepresent the
actual content [10].
Finding 4: The root causes of recovery failures are diverse.
It is known that error handling deficiencies (i.e., missing
or incorrect handlers) are a common source of recovery fail-
ures, which account for 28% of the studied cases. In our
study we found that state management issues (37%) turns
out to be the most common root cause, stemming from im-
proper synchronization or invalid handling of recovery state.
In one case of Mesos [ 31], parent-child container relation-
ships were mismanaged during recovery—intended to restore
container state—resulting in agent node crashes. Another
common cause is inappropriate resource lifecycle manage-
ment (13%), which arise from incomplete cleanup of system
resources; for example, unclosed files in the error handler led
to resource leaks [ 13]. We also observed recovery exhaust
system resources (9%) such as too frequent retries and other
implementation flaws (6%) leading to failed recovery.
Finding 5: Most recovery failures (92%) manifest beyond
local thread scope.
While some studied failures are confined to a single thread,
most of them Inter-thread (30%) involve coordination be-
tween threads within the same process. HDFS-16115 [ 21]
illustrates this case, where a faulty error handler in one thread
caused command pileup in another thread, leading to zombie
operations. Inter-process (35%) affect coordination across
processes in distributed system; in KAFKA-10832 [28], im-
proper recovery handling by a broker corrupted the producer
node’s state. The most complexInter-service (27%) span mul-
tiple services. as in TiDB-963 [38], misinterpreted failures led
Kubernetes’s recovery to incorrectly scale TiKV instances.
Finding 6: 63% of recovery failures are avoidable with minor
tweaks to original recovery.
Surprisingly, we found that many recovery failures could
have been prevented without complex strategies. Tolerating
non-critical errors during recovery (19%) would allow the
recovery to complete successfully without introducing fur-
ther problems. Some recovery failures only manifest under
specific event orderings, and developers may manually en-
force or bypass certain sequences to ensure correct behavior
(12%). In one incident [ 34], RabbitMQ’s HA failover re-
covery would fail if health checks ran during master node
promotion. The developers fixed this by manually enforcing
health checks after master election is complete. Rebalancing
recovery workloads across the system (18%) can help miti-
gate recovery induced overload, such as avoiding transferring
all write-ahead log (W AL) queues from a failed RegionServer
to a single live server through distributing replication queues
more evenly [8]. Finally, changing recovery-related configu-
rations or parameters (14%) may also help.
2.2 Implication
While simulating recovery actions in situ may appear ambi-
tious, our study findings highlight that it is both necessary
and feasible. The persistence and severity of recovery fail-
ures (Findings 1-3) highlight that such issues are widespread
and pose critical challenges requiring immediate attention.
However, standard testing environments often miss these root
causes due to diverse root causes (Finding 4). The opportu-
nities of better recovery strategy (Finding 6) underscores the
need for a technique that allows systems to safely evaluate
the consequences of recovery actions before applying them.
Finally, recovery actions frequently involve cross-thread and
cross-process interactions (Finding 5). This insight requires
the solution to simulate complex recovery behavior across
system boundaries.
3 Simulating Recovery with Pilot Execution
3.1 Design Goals
Motivated by our study findings, we propose a new execu-
tion model, pilot execution, to predict recovery failures. Pilot
execution provides lightweight, sandboxed execution con-
texts that simulate recovery logic in situ—within the live dis-
tributed system—without introducing side effects. It enables
3

## Page 4

Conference’17, July 2017, Washington, DC, USA Submission # XXX
ZooKeeper 
/hbase/rs/ip1:host 
Region 
Server1 
HMaster 
RegionServer2 Region 
Server3 
HDFS 
/rs1/wal/region/.recover.edits/ 
Replication 
Source (t1) 
ReplicationWAL 
Reader (t2) 
Replication 
Source 
Shipper (t3) 
Replication 
EndPoint (t4) 
HBase 
Cluster 
CRASH! 
RegionServer 
Tracker 
/rs2/wal/region/.recover.edits/ 
t1’ t2’ t3’ t4’ 
/rs2/wal/region/.recover.edits/ 
NPE! 
NPE! 
original 
execution 
pilot 
execution 
Figure 2. Overview of recovery process in HBase-25898. chang: in graph try to highlight key elements: phantom threads, propagation, I/O
redirection
systems to evaluate the consequences of recovery actions be-
fore those actions are applied, thus offering a new level of
safety and foresight in cloud operations.
chang: add a paragraph to clarify challenges? (or in the
intro)
chang: what is guaranteed?
Scope and Assumptions We target risky recovery logic in
distributed systems, especially those prone to complex cross-
thread/process interactions. Pilot execution runs on the same
binaries and configuration as production and observes live
state while redirecting all writes (files/DB/queues) and prox-
ying external calls to shadow channels so that no externally
visible side effects occur. We assume we can track most of
explicit interactions by tagging and propagating a context
packet across thread pools, async callbacks, and RPC bound-
aries. We also assume access to source/bytecode for selective
instrumentation. Pilot runs must terminate within a bounded
window, returning signals for commit/abort/revise.
3.2 Workflow
A pilot run is a single instance of pilot execution parameter-
ized by an entry point ri and a policy (time budget, limits,
stop conditions). A run:
• starts at ri under the policy; futures/callbacks, and RPC/queues;
• mirrors the recovery path on phantom threads so production
scheduling and state are untouched;
• propagates a pilot context across thread pools,
• isolates side effects via state shadowing and proxy layer;
• observes exceptions, timeouts, resource curves, and semantic-
checker violations in a unified event stream;
• terminates within budget and emits commit/abort/revise
signals, then reclaims shadow resources.
At the core of this model is a new abstraction called phan-
tom threads, which at the thread level mirror recovery logic
without interfering with live execution.
3.3 Enabling Mechanisms
chang: mention somewhere our approach requires two basic
mechniasm to work: static instrumentation and runtime design
Context Propagation Modern recovery logic is rarely con-
fined to a single thread or component. Our execution frame-
work is equipped with a lightweight context propagation
mechanism that ensures recovery effects can be tracked across
thread pools, asynchronous tasks, and even remote services.
This is achieved through automatic instrumentation of re-
covery paths and metadata injection at multi-level commu-
nication boundaries, allowing end-to-end simulation across
distributed environments.
State Shadowing and I/O Redirection To ensure safety,
pilot execution proceeds within a sandboxed environment
that isolates their effects from production. This isolation is
enforced across multiple layers. At the state level, relevant
memory structures are duplicated through shallow copies
and pointer redirection to prevent unintended mutations. I/O
operations, including file access and network communication,
are rerouted to proxy layers that simulate their effects without
reaching external systems. The system additionally intercepts
and sanitizes unsafe system calls at the system level to avoid
triggering destructive behavior.
3.4 Example
In Figure 2, we illustrate how the pilot execution model han-
dles the motivating HBase example. When the system encoun-
ters the error signal of RS1 crash, a special handler intercepts
the exception before it can impact live servers. This triggers
a new round of pilot execution initiated from the HMaster,
which sends an RPC to RS2 using the original RPC interface.
What sets it apart from original recovery is that, the request
is encoded with metadata identifying it as part of a pilot ex-
ecution. Upon receiving the request, RS2’s handler detects
the pilot context and diverts the execution into a special “pi-
lot mode,” where all operations are executed by a dedicated
group of phantom threads. These phantom threads isolate side
effects from the production environment. For example, any
updates to HDFS are redirected to a parallel shadow copy
that is only visible to components running in pilot mode. The
recovery logic proceeds as it would in a real run, ultimately
triggering the same failure conditions. Meanwhile, because
all side effects are contained, the system can safely observe
4

## Page 5

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
public  class  RegionServerTracker extends  ZKListener  {
  public  void  nodeChildrenChanged (...)  {
+   PilotContext c = PilotUtil.start( 
+       this:: nodeChildrenChanged$pilot, conf, policy); 
+   if (PilotUtil.waitFinishOrAbort(c) && 
+         PilotUtil.observe(c).status == FAILED){ 
+       if(policy.revise) { 
+         PilotUtil.decide(c, STATUS_REVISE, new_conf);} 
+       PilotUtil.decide(c, STATUS_ABORT); 
+       PilotUtil.report(c); return;    
+   } 
+       PilotUtil.decide(c, STATUS_COMMIT); 
    if  (path.equals(watcher. getZNodePaths ().rsZNode) 
      && !server. isAborted () && !server. isStopped ()) 
      executor.execute(this:: refresh ); 
  } 
1
2
3
4
5
6
7
8
9
10 
11 
12 
13 
14 
15 
16 
17 
Figure 3. Codes of enabling PILOT in the HBase example.
the failure signal and use this insight to adjust the mitigation
strategy—such as deleting the problematic WAL—without
risking further disruption. After the simulation completes, the
phantom threads are safely recycled, ensuring the live system
remains unaffected throughout the process.
4 Pilot Execution Design
4.1 Interface
We show PILOT interface in Table 2. The PILOT runtime
library is responsible for creating and managing all pilot
runs throughout their lifecycle. We use the code example in
Figure 7 to walk through the usage.
nodeChildrenChanged is the recovery entry for our moti-
vational example from HBase. Developers first add a start
call to initiate a new pilot run. The runtime assigns a globally
unique epoch ID and registers it in PILOT key-value storage
under /pilot-runs/<id>. This epoch id will be used to detect
if multiple pilot runs concurrently exist. It also registers re-
sources related to this run such as executing thread ID using
a map structure.
The execution then blocks atwaitFinishOrAbort. This block-
ing call avoids two concurrent recovery (original and pilot)
interfere with each other. It continuously monitors the re-
source allocation status to detect pilot execution completion.
This function waits until all execution units are removed
from /pilot-runs/<id>. Meanwhile, developers have access
to events and errors during pilot execution via observe.
When a pilot run finishes, waitFinishOrAbort unblocks
and execution proceeds in the original thread. Based on the
result and the pre-defined policy, the program may choose
to continue the recovery process (if the pilot run returns suc-
cessful results), abort (if severe consequences were exposed
during the pilot run), or revise the configuration and rerun (if
the policy permits). Optionally, the system outputs a summary
of the pilot run which includes exceptions, time durations and
resource usage via report(..) call.
4.2 Managing Pilot via Phantom Threads
The goal of a pilot run is to rehearse recovery paths without
interfering with other worker threads. Running the recovery
phantom 
thread 
f1 →f2 original 
thread 
➊ 
➋ ➌ $➍
start(..) 
pilot state 
manager 
block until 
all ﬁnish 
/pilot-runs/1/t1 
waitFinishOrAbort(..) 
/pilot-runs/1/t1 
f3 
f1 →f2 →f3$pilot 
Figure 4. Lifecycle of phantom threads.
logic on the original thread would block or perturb normal
service, and makes rollback hard; using process fork/contain-
ers is heavy and inconvenient to observe real-time system
states.
To address these limitations, we realize pilot execution by
spawning and mirroring execution on a group of phantom
threads, which are ephemeral, in-process execution units that
rehearse a prospective recovery path without changing the
behavior of production threads. Phantom threads strike the
middle ground: they remain inside the address space to share
code and state (in a read-only way) while lightweight and
easy to control side effects.
4.2.1 Lifecyles of Phantom Threads We show the com-
plete lifecyle of a phantom thread in Figure 4. Phantom
threads are created on-demand. A typical example is when
a new pilot run is activated via start call (❶). The caller
API prepares the thread creation by copying thread states and
recording call stacks. This is because the new thread needs
to be “fast-forwarded” to the exact same state as the orig-
inal thread. The newly created phantom thread recursively
traverse each layer in the call stack. Instead of replaying the
original codes, it restores local variables from the call stack
through copying and pops the corresponding frame. This pro-
cess repeats until the call stack is empty—precisely at the call
site where the start is invoked. While the fast-forward func-
tion can be realized by modifying language runtime, PILOT
chooses to build this function via static instrumentation for
better generality. Similar to the registration procedure for pi-
lot run metadata, a new phantom thread also needs to register
its thread id at the state manager (❷), so PILOT runtime can
keep track of its lifecycle.
chang: this part still sounds a bit magical, will need to
add more details of our implementation based on notion note,
essentially 1) how we implement micro-fork 2) what precisely
need to be instrumented
Besides explicitly calling start, new phantom threads may
also be created when another phantom thread propagate. For
example, a phantom thread sends a network request to another
node and initiate a new flow on the remote side. We will
discuss these scenarios with more details in § 4.3.
Inside phantom threads, the execution runs a transformed
version of functions which are different from the original
thread. This is because a pilot run is designed to be a sim-
ulation thus we should not directly use original functions,
especially those cause dangerous effects ( e.g., rebooting).
5

## Page 6

Conference’17, July 2017, Washington, DC, USA Submission # XXX
API Description
RunId start(EntryPoint r, Policy pi) start a pilot run at entry point r under policy pi (e.g., time budget, stop conditions).
void observe(RunId runId, Consumer<Observation> sink) stream observations (events, exceptions, resource curves, invariant violations) tosink.
Status decide(RunId runId, Decision decision) submit a decision grounded in current observations; returns updated run Status.
Status waitFinishOrAbort(RunId runId) block until the pilot execution finishes or aborts; return the terminal Status.
Summary report(RunId runId) retrieve a summary (path coverage and critical events) for the run.
Table 2. Pilot APIs.
We need additional instrumentation points for observability
(e.g., inject at shutdown call to produce an alerting event). We
explain how we transform original functions to pilot version
when discussing ensuring side-effect isolation in§ 4.4.
At the end of execution phantom threads need to be termi-
nated, otherwise they will run indefinitely and waste system
resources (and more importantly, block normal recovery).
PILOT runtime keep tracks of them by monitoring resource
status registered in the key-value storage. When a phantom
thread exit, its associated ID is removed from storage to up-
date its status (❸).
After a phantom thread exits, the original thread does not
immediately resume execution. PILOT runtime is responsible
to make the decision to alter the execution back. It periodically
checks to align the status data in the state manager to current
execution thread states. Once it found all threads under a
pilot run has finished (or aborted), it notifies the blocking call
waitFinishedOrAbort to resume execution (❹).
Phantom threads’ liveness is bound to registration data
bidirectionally. Developers may abort a pilot run by invok-
ing APIs which deletes thread registration data in key-value
storage, triggering callbacks on all nodes to clean up the corre-
sponding threads. Additionally, each pilot run has a maximum
time budget. A timeout mechanism always recursively cleans
up the root node and its children nodes in storage associated
to a pilot run when the timer fires.
4.2.2 Handling Synchronization As phantom threads run
concurrently with original threads, race conditions may occur.
For example, an original thread t and a phantom thread t′
may simultaneously require the same lock L. If we allow
t′ to acquire the lock, it blocks the normal execution of t
thus violating our safety guarantee. Meanwhile, completely
ignoring the locking semantics produces inaccurate pilot run
results as some recovery operations need to wait until certain
conditions.
To ensure accurate pilot runs without interfering with live
execution, we introduce a speculative locking mechanism.
The core principle is that phantom threads acquire locks
“speculatively” — they always yield to original threads on con-
flict, immediately aborting pilot execution when contention
is detected. This guarantees non-interference with production
execution, at the cost of incompleteness. It deals with four
different scenarios:
• Only original threads: Synchronization primitives behave
same as originals.
• Only phantom threads: Synchronization primitives behave
same as originals.
• Phantom held the lock, original acquire: The phantom
thread releases the lock and pilot execution terminates im-
mediately to avoid inaccurate results.
• Original held the lock, phantom acquire: If an original
thread t1 holds the lock, a phantom thread t2 waits until t1
releases it. This wait does not block other original threads;
for example, if another original thread t3 acquires the lock
during the pilot run, the pilot execution aborts.
PILOT implements this mechanism by adding an auxiliary
queue to each lock and instrumenting the synchronization
primitive interfaces. We show the logic in Algorithm 4. It
maintains three state variables: lockSeq is an atomic integer
which marks the sequence id for the next acquire. curren-
tHolder is an atomic integer which marks the sequence id
of the current lock holder. delegate points to the original
lock. An original thread simply acquires the real lock ( del-
egate) and runs as usual, aborting any ongoing pilot run if
phantom threads are queued or active. A phantom thread,
when requesting the lock, takes a sequence number from
lockSeq and waits until it is its turn and the real lock is free
(checked via ISLOCKED (delegate)). Once both conditions
are satisfied, the phantom enters a speculative critical section
without touching the real lock. When it finishes, it increments
currentHolder so the next phantom can proceed. This ap-
proach ensures original threads are never delayed, phantoms
execute in FIFO order, and any potential conflict with real
execution is avoided.
4.2.3 Fault Tolerance PILOT runtime may include bugs
and results in faults. We consider two types of faults to handle.
First, PILOT uses registered nodes in storage to trigger
cleanup callbacks for resource recycling. Thus, it is crucial
to ensure the correctness of registered status data. To prevent
such issues, PILOT implements a distributed key-value stor-
age with a third-party coordination service ZooKeeper [ 1].
ZooKeeper guarantees consensus between phantom threads
across different servers on if a pilot run is still active or not.
Still, it is possible to leave dangling nodes if relying on
threads explicitly deleting nodes by themselves. For this rea-
son, we implement the automatic recycling mechanism de-
scribed using ZooKeeper’s Time-to-Live node [32]. Unlike
default persistent nodes which remain until explicitly deleted,
TTL nodes are automatically removed after a specified time
period if they have not been modified. PILOT runtime and
6

## Page 7

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
Algorithm 1: Speculative Lock
1: State Variables:
2: lockSeq ← 0, currentHolder ← 0, delegate ← original lock
3:
4: procedure ACQUIRE_LOCK(t)
5: if t.state = ORIGINAL then
6: LOCK (delegate)
7: if lockSeq > currentHolder then
8: ABORT PILOT RUN()
9: else if t.state = PHANTOM then
10: t.mySeq ← lockSeq
11: lockSeq ← lockSeq +1
12: while (currentHolder < t.mySeq) ∨ ISLOCKED (delegate)
do
13: YIELD
14:
15: procedure RELEASE_LOCK(t)
16: if t.state = ORIGINAL then
17: UNLOCK (delegate)
18: else if t.state = PHANTOM then
19: currentHolder ← currentHolder + 1
ZooKeeper cross-check to guarantee status is consistent and
would be recycled properly.
The other potential issue is a storm of phantom threads,
created by cascading creation of phantom threads in a positive
feedback loop. PILOT runtime addresses this issue by record-
ing thread dependencies and identifying cycles when creating
new phantom threads. For example, if it found cyclic struc-
tures such as T1 → T2 → T3 → T1, it pauses the creation of
new phantom threads and reports such violation as a critical
event. Additionally, there is a upper bound for the maximum
number of concurrent phantom threads running in the system
to prevent a pilot run from exhausting system resources.
Note that faults here refer to those from PILOT itself. We
will discuss isolating faults in execution in § 4.4.
4.3 Propagating Pilot Execution
Recovery logic often spans across multiple threads and pro-
cesses. When pilot execution crosses such boundaries (e.g.,
making an RPC call), the system ensures that the execution
continues under phantom threads and keeps track of these
threads for proper management.
4.3.1 Context-based Propagation Inspired by prior dis-
tributed tracing works [78, 79], we design a context-propagation
mechanism to track pilot execution. The core idea is to main-
tain lightweight metadata that travel with any execution, whether
to another thread, a different process, or an external service.
Our runtime automatically captures the context at the source,
propagates it through the handoff boundary (e.g., wrapping
APIs, injecting headers), and activates pilot execution on the
destination side by creating an isolated phantom thread.
PILOT initializes a lightweight PilotContext when a pilot
execution begins and attaches it to the originating thread as
thread-local metadata. The context records a unique pilot ID,
thread1 
func1 
func2’ 
func1’ 
func3’ 
thread2 
func4 
func4’ 
job queue 
thread3 
func5’ 
func5 
func6’ 
sync 
primitives 
process1 
➊ 
➍
process2 
func1 …
process3 
func1 …
3rd-party service 
➋
RPC 
listen 
func7 
func7’ 
func8’ 
shared 
vars 
thread4 
➌
➎
Figure 5. Propagating pilot execution across thread and process
boundaries.
the recovery action and callsite that spawned it, and minimal
lineage needed to track subsequent handoffs ( e.g., parent
pilot ID and a local epoch). This metadata is intentionally
compact so it can be propagated cheaply; it carries just enough
information for the destination to (i) recognize that the request
originates from a pilot execution, (ii) resume in pilot mode
under a phantom thread, and (iii) report provenance back to
the runtime for bookkeeping and eventual teardown.
PilotContext is a thread-local key value map for metadata,
it includes: (1) a globally unique pilot ID identifying the ex-
ecution round, enabling any thread to determine execution
mode—a non-null pilot ID indicates phantom thread execu-
tion, triggering redirection to pilot-version functions, while
null indicates original thread execution; (2) span metadata
for tracing pilot execution—each contains span-related fields:
spanID (unique identifier for current execution segment), par-
entSpanID (linking to the parent span), and startTimestamp
(for timeout management). Whenever propagation occurs
across thread or process boundaries, a new span is created
with a fresh spanID, while inheriting the sender’sspanID as its
parentSpanID. This parent-child linkage builds an execution
tree that tracks the complete recovery path;
On the receiving side of a handoff, PILOT examines the
incoming metadata; if a valid PilotContext is present, it ac-
tivates pilot mode by creating or reusing a phantom thread
and binding the context to it. The handler then executes pilot-
version code paths while the runtime records a lineage edge
from the sender to the newly activated unit.
4.3.2 Cross-Thread/Process Scenarios We demonstrate
five currently supported patterns in Figure 5
Task–Executor Model (❶). Many recovery actions enqueue
asynchronous tasks that later run on executor threads, which
breaks the direct thread lineage and, by default, loses pi-
lot intent. PILOT instruments standard task interfaces ( e.g.,
Runnable/Callable/Future) to carry a context from the sub-
mitting pilot thread. When the task is executed, the runtime
inspects the context: if valid, it activates a phantom thread and
redirects to pilot-version handlers; otherwise it runs normally.
Synchronization Primitives (❷). Coordination via condi-
tion variables, latches, and similar primitives transfers control
across threads in ways that can make pilot-induced wake-
ups affect originals. PILOT replaces common synchronization
7

## Page 8

Conference’17, July 2017, Washington, DC, USA Submission # XXX
primitives with wrapper variants that record waiters/signallers
and carry context. When a phantom thread signals, the wrap-
per dequeues the next waiter: if it is an original thread, PILOT
performs a micro-fork bound to the signaling context, con-
tinuing the awakened path under a phantom thread. It turns
the wrapper’s wait queue into an explicit propagation bridge
while preserving isolation of originals.
Shared Variable Monitoring (❸). Systems often have threads
that poll or branch on shared variables that pilot execution
may update (e.g., status flags), implicitly handing off control
through shared state. PILOT uses static analysis to identify
such variables (typically lock-protected or concurrent types),
augments them with an embedded PilotContext slot, and
injects a guard at access sites. When a pilot write marks a
variable, subsequent original-thread reads triggers to switch
the affected code path into pilot mode under a phantom thread.
Synchronous Cross-Process/Service (❹). RPC/HTTP bound-
aries sever thread identity and process state, so pilot intent
must traverse message channels. PILOT injects PilotContext
into outbound metadata (e.g., HTTP headers, gRPC metadata,
or custom RPC fields), piggybacking on standard interceptors
or extending existing serialization hooks. At receiver entry
points (e.g., servlet filters, gRPC service stubs), the runtime
detects the context, spawns or reuses a phantom thread bound
to it, and dispatches pilot-version handlers.
Asynchronous Cross-Process/Service (❺). Some third-party
services (e.g., ZooKeeper) deliver callbacks asynchronously,
where the causality between a pilot-originating write and
a later watch event is not explicit. PILOT introduces a thin
client-side proxy: on pilot-originating operations it persists
the current PilotContext to a side metadata channel (e.g., a
sibling znode), and on watch delivery it intercepts the call-
back, retrieves the matching context, and activates a phantom
thread to handle the event in pilot mode.
4.4 Isolating Induced Side-Effects
Pilot execution runs recovery logic in situ; without careful
isolation, its side effects could leak into production state
or third-party services and, conversely, over-isolation could
make the pilot result unfaithful. In this section we discuss
the isolation problem and our solution around two domains:
program states and I/O.
4.4.1 Shadowing System States We must ensure that pilot
execution leaves no persistent changes to critical system state.
Two standard strategies are often considered: state duplication
and transactional rollback. Duplicating state via full copies or
snapshots roughly doubles memory (and copy) costs, which
is impractical in production. Transactional rollback presumes
updates are cleanly encapsulated as transactions; in many dis-
tributed systems, state changes are spread across ad-hoc data
structures and services, so there is no uniform transactional
boundary to revert reliably.
Our design chooses the first (copying) approach, and ex-
ecutes it in a selective and lazy way. Our key insight is that
recovery actions usually touch only a small fraction of state,
so there is no need to clone whole objects or graphs. In-
spired by copy-on-write (COW), we adopt selective shad-
owing: on first access, we create a shallow reference for the
specific field and redirect all subsequent reads/writes to that
shadow. Nested objects are materialized only when they are
actually touched. For instance, when a pilot function modifies
field.sub1.sub2, modification is recursively redirected to its
shadow counterpart field.sub1.sub2$shadow instead of du-
plicating the whole field. We find this design is particularly
useful when applying to large data structure such as HRe-
gionServer (commonly used in HBase). This keeps memory
overhead low, preserves internal read-after-write behavior,
and prevents any writes to production state.
4.4.2 Redirecting I/O Pilot execution must be hermetic:
its effects stay within the simulated environment and never
reach the external environment (local file systems, distributed
stores, or third-party services). We require scoped isolation:
pilot side effects are invisible to production yet fully visible
within the pilot run. All pilot I/O is transparently redirected
to pilot-scoped namespaces: for example, a file write by one
pilot thread is seen by other pilot threads while the original
thread continues to observe the unmodified file.
To isolate file system side effects during pilot execution,
PILOT intercepts file operations and redirects them to a dedi-
cated shadow directory. Rather than eagerly duplicating origi-
nal files to shadow directory, PILOT employs a lazy copying
strategy: it initially replicates only the directory structure and
metadata, deferring actual data copying until necessary.
This lazy copy optimization targets at scenarios where
recovery does not exhibit read-after-write behavior. When a
pilot writes to an existing file, PILOT avoids making a full
copy and instead appends changes to a separate log. Only if
the file is subsequently read during pilot execution does the
system reconstruct it by replaying the log over the original
content. For files that are only written but never read back, this
strategy significantly reduces I/O overhead. However, when a
read is triggered, we still have to pay the cost of copying the
original file and apply the append log on top of it.
Newly created files during pilot execution are written di-
rectly into the shadow environment. Since they have no pre-
existing version to preserve, no append log is used. Reads
simply access the latest content in the virtual file system,
maintaining isolation without extra overhead.
For third-party libraries, we apply a similar approach by
redirecting all operations to isolated namespaces under a
pilot-specific prefix ( i.e., /pilot/...) that are only visible
within pilot execution. We abstract the client-side operations
of those third-party services into read/write operations and
intercept the API calls. We also apply lazy copy optimization
described above in I/O isolation to further reducing the over-
head. Supporting more complicated operation semantics such
as watchers in ZooKeeper remains a part of future work.
8

## Page 9

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
4.5 Observing and Reacting to Failures
PILOT runtime embeds monitoring components, which eval-
uate the effectiveness and impact of recovery actions before
deployment. To assess feasibility, the system checks if the
same error persists during pilot execution, indicating recov-
ery failure. A timer measures recovery duration and system
downtime. Resource cost is tracked through memory and I/O
usage changes from checkers. For side effects, checkers detect
new error signals and monitor system health metrics, such as
node availability and request throughput, with support from
existing runtime checking tools [52, 74, 75].
Using the same context propagation mechanism in § 4.3,
PILOT records each pilot-scoped function/RPC as a span and
links spans by caller–callee to form a cross-thread/process
execution tree in the style of distributed tracing [78, 79]. Each
span has a unique ID, its parent pointer, and minimal metadata
stored in and carried by the context. Runtime monitors mark
the active span when they observe anomalies (e.g., exceptions,
timeouts, or resource-limit violations). Upon a failure, the
PILOT runtime materializes the tree and the precise path from
the pilot entry point to the error, capturing which components
were involved and how effects propagated.
To enable iterative re-runs with different parameters, we
expose a revise-and-rerun interface: after a pilot run com-
pletes via waitFinishOrAbort(runId), the controller calls de-
cide(runId, REVISE) to launch a fresh run at the same entry
point with configuration deltas (e.g., throttling, batch size)
and optional policy updates (time budget, stop conditions).
The runtime terminates the old run, and starts a new run with
the updated ID. Operators then use observe(newRunId) to
monitor metrics, anomalies, and traces.
4.6 Enabling Lightweight Pilot Execution
Recovery should be prompt to reduce system downtime. While
it may seem advantageous to reduce actions during pilot exe-
cution to accelerate recovery, we argue that this compromises
the accuracy of the emulated results. Instead, we propose
reducing recovery delays by “warming up” the system during
pilot execution, enabling a rapid transition to “fast replay”
during actual recovery. We observe that bottlenecks often
stem from time-intensive operations such as reading/writing
large log files, transferring bulk data over networks, and ini-
tializing new instances. Thus, we caches intermediate results
to mitigate these delays.
4.6.1 Caching I/O Operations Recovery frequently re-
quires transferring large data volumes between nodes. Pilot
execution performs these transfers but stores them in isolated
locations. Upon committing recovery, we avoid redundant
transfers through checksum validation. Consider Solr’s recov-
ery example: when the operator tries to recover a failed fol-
lower node, it must download files from leader nodes through
network stack to synchronize. During pilot execution, the
failed follower node downloads these files to isolated direc-
tories and records checksums. When actual recovery begins,
the node first query the remote checksum. If unchanged, it
simply rename the cached files from the isolated directory
to production paths—an O(1) operation replacing network
transfer.
4.6.2 Caching Deterministic Computations Many recov-
ery computations are deterministic—given identical inputs,
they produce identical outputs. PILOT mark functions as
cacheable if they have no side effects beyond return values,
access only immutable or versioned state, and contain no
non-deterministic operations. For Cassandra’s MerkleTree
operations, the difference computation between two trees is
purely functional—it reads tree structures and produces a list
of differing ranges without modifying any state. During pilot
execution, PILOT computes a hash of the function’s inputs
and stores the result indexed by this hash. During actual re-
covery, if the input hash matches, we return the cached result
directly, eliminating redundant computation. Both in-memory
and on-disk cached intermediate results persist across pilot
executions until their lease expires or they are explicitly dis-
carded, after which the PILOT runtime (e.g., file deletion)
cleans them up.
9

## Page 10

Conference’17, July 2017, Washington, DC, USA Submission # XXX
4.7 Compiler Support
Identifying Recovery Entries PILOT begins the automa-
tion process by identifying recovery entries to insert systems
APIs. chang: def Recovery entry points fall into two cate-
gories: passive and proactive. Passive handlers include error-
handling constructs (e.g., try-catch blocks) and listeners for
third-party services (e.g., ZooKeeper). Proactive handlers are
typically implemented as CLI commands, such as Cassan-
dra’s nodetool repair. Both of them have a clear pattern.
PILOT further filters recovery entries with simple (e.g., just
logging the error message) or even empty handling logic.
Once an entry point is identified, PILOT instruments the
code to divert execution into pilot mode. As shown in Figure 7,
..
Converting f → f ′ chang: what do we do to convert these
functions?
[Add hooks for context propagation]
5 Implementation
Our tool uses Soot [97] as the backend framework for static
analysis and instrumentation. We implement our metadata
propagation based on OpenTelemetry [33]. While our current
implementation is based on Java, our techniques does not rely
on language-specific features and can be conveniently ported
to systems based on different languages. The tool includes a
single script which automates the static transformation work-
flow and prepares the program package.
6 Evaluation
In this section, we conduct a comprehensive evaluation of
our PILOT approach to address several crucial questions: (1)
can PILOT successfully enables pilot execution for real-world
distributed systems; (2) can PILOT detect recovery failures
before they happen; (3) can the results of PILOT detection
prevent failures happening; (4) what are the static and runtime
overheads incurred by PILOT . The experiments are done in
servers with 8 cores 2.0 GHz CPUs, 64 GB memory, running
Ubuntu 22.04.
6.1 Manual Effort of Using P ILOT
Most analysis and instrumentation by PILOT is automatic. PI-
LOT requires a configuration file for each system to highlight
metadata such as source file path to guide the static analysis.
Additionally, many distributed systems implement custom
protocols and require minor modification to our implementa-
tion of inserting context metadata into message headers when
propagating through processes. These manual changes are
41 lines of code in Cassandra, 89 in HBase, 50 in Hadoop
(HDFS and Yarn share the same RPC framework). Solr used
standard HTTP library for communication so there is no need
for manual moification.
System Version Lines of Code (LOC)
Solr 8.11.4 650K
HDFS 3.0.0 550K
Cassandra 4.0.0 435K
HBASE 2.5.12 1220K
Y ARN 2.9.0 442K
Table 3. Size of five evaluated systems.
System Candidate EP. Total EP. Dedicated Thread.
Solr 26 1700 4
HDFS 12 556 6
Cassandra 34 2216 5
HBASE 60 1561 29
Y ARN 24 1247 9
Table 4.Numbers of identified entry points in each system. EP=entry
points
6.2 Applying P ILOT to Real-World Systems
To evaluate the practicality of our approach, we appliedPILOT
to five real-world distributed systems: Solr, HDFS, Cassan-
dra, HBase and YARN (Table 3). These systems are widely
deployed in production and are known to suffer from subtle
recovery-related failures, many of which are hard to catch
using traditional testing or modeling techniques. Their wide-
spread use and complex recovery paths make them ideal case
studies for demonstrating how pilot execution can surface hid-
den faults. PILOT successfully enabled pilot execution for all
five systems. In Table 4, we show how many starting points of
pilot execution are identified based on pattern matching and
filtered based on our heuristic rule, demonstrating that PILOT
successfully limits the scope of recovery checks to minimize
runtime overhead. We also show how many threads require
hook insertion for micro fork.
6.3 Runtime Detection and Recovery
Methodology PILOT is designed to be a simulation tool to
expose recovery failures before happening. The key metric
for evaluating it is once the recovery action is triggered in
a running system and will cause a failure, whether and how
quickly can the tool detect the failure. This contrasts with bug-
detection tools (e.g., fuzzing), which are designed to induce
bugs by generating triggering conditions like crafted inputs
or specific thread interleavings.
Failure Benchmark We collected and reproduced twenty
real-world recovery failures from five systems: Solr, HDFS,
Cassandra, HBase and Y ARN. Table 5 shows the list of eval-
uated cases. All of these failures led to severe consequences.
Each case took one week on average to reproduce. Note that
80 percent of cases are not included in the earlier study.
6.3.1 Detecting Recovery Failures
Setup We evaluated PILOT against the following baseline
methods.
• We design an A/B testing strategy by configuring the system
so that instead of applying recovery actions to all nodes,
they are only applied to a certain range of nodes (e.g., single
10

## Page 11

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
Id. Feature Symptom Studied
SL1 [36] Follower recovery Crash N
SL2 [35] Follower recovery Timeout N
SL3 [37] Core recovery Cluster Outage N
HF1 [22] Namenode failover Crash Y
HF2 [24] Error handler Exit abnormally N
HF3 [19] Error handler Incorrect Results N
HF4 [16] Datanode recovery Crash N
HF5 [23] Datanode recovery Partial Failure N
CS1 [2] Node recovery Crash(cascading) N
CS2 [3] Node recovery Out-of-Memory Y
CS3 [5] Inconsistency Timeout N
CS4 [4] Inconsistency Timeout N
HB1 [15] Snapshot Recovery Inconsistent States Y
HB2 [9] RegionServer failover Partial failure N
HB3 [12] RegionServer failover Crash (cascading) Y
HB4 [11] Scan Retry Crash (cascading) N
YN1 [42] ResourceManager failover Crash Y
YN2 [40] ResourceManager failover Crash N
YN3 [41] NodeManager Recovery Exit abnormally N
YN4 [39] NodeManager Recovery Crash N
Table 5. 20 real-world recovery failures used in our evaluation. SL:
Solr; HF: HDFS; CS: Cassandra; HB: HBase; YN: Y ARN.
range mode in Cassandra), allowing the system to observe
the consequences before a full roll-out.
• We use the system’s built-in dry-run feature in the exist-
ing admin tool. For example, Cassandra node repair tool
provides a preview option to list data ranges with inconsis-
tencies before attempting to fix them. For systems without
built-in dry-run features, we provide an ad hoc implemen-
tation that only outputs the recovery plans without actually
performing them.
• We extended the failure detector from a related work [90].
We adapted the tool by enhancing its log collection and
correlation mechanisms to better support recovery-related
failures, especially those that cascade across components.
• We adapted a validation framework from related work [81]
by modifying its trace-based replay mechanism to support
recovery-specific validation.
Results [Update already] The results are shown in Table 6.
PILOT successfully detected seventeen out of twenty evalu-
ated issues, exposing a broader range of failures. In contrast,
baseline approaches, even all four combined only detect nine
failures. For A/B testing, while it can sometimes expose the
failures, they are non-deterministic and highly depend on how
the nodes of test set are selected. For example, for CS3 and
CS4, the timeout-related issues could only be triggered if
the specific problematic node is included in the selected test
group. Additionally, if A/B testing fails, it often either leaves
the faulty node in corrupted or undefined stage, or still caus-
ing a cascading failure. In HB3, the failure of the test node
triggers additional recovery and affects other nodes, causing
them to fail in a cascading manner. The built-in preview does
reveal some issues. However, the preview only includes the
recovery plan preparation step and is often limited to expose
issues in the actual recovery step, which is not executed dur-
ing preview. The vicious cycle detector is specifically good at
retrying-style issues while other types of failures are beyond
its scope.
[Note: This paragraph maybe compressed] Based on our
evaluation (Table 5), we found that A/B testing can trigger
cascading failures that spread beyond the intended test sub-
set like HB3. Since distributed systems are interconnected,
failures during recovery testing can create unexpected load
patterns, timeout cascades, or dependency failures that affect
other system components, ultimately leading to broader sys-
tem instability. Moreover, A/B testing cannot fully guarantee
that its results are correct because the test subset represents
only a sample, and conditions in complex distributed environ-
ments may not be entirely consistent across all replicas. This
is also why A/B testing does not expose most of the issues in
our evaluation (Table 5).
6.3.2 Recovering from Failures
Setup We evaluated each issue under five scenarios. We
first evaluate in the buggy version, the time from the start
of recovery until a recovery failure manifests without ( ❶)
and with pilot execution ( ❷), which shows how fast pilot
execution exposes the issue compared to directly performing
recovery. We then measure, in the correct version which fixed
the issue in the recovery code, whether pilot execution will
incur significant delay by comparing recovery time without
pilot execution (❸), with pilot execution (❹), as well as total
time if the system decides to commit the recovery action once
the pilot execution proves safe (❺).
Results Table 7 summarizes the evaluation results. Under
the execution with buggy version, pilot execution takes a
similar amount of time compared to the original recovery,
incurring 4.38% latency increase on average. Under the ex-
ecution with correct version, we found that the combination
of base and pilot execution incurs additional latency ranging
from seconds to dozens of seconds. Thanks to our caching
optimization mechanism, the actual recovery after pilot ex-
ecution is accelerated, thus the total time is much smaller
than the sum of running two phases individually (TODO%
less). We consider the performance is still comparable and
the overhead is a worthwhile tradeoff for the effectiveness
and safety assurance we received with this approach. For HF3
and HB4 we are unable to collect its recovery latency under
the correct version as the code fix removes the whole error
handling logic.
6.4 Preventing Recovery Failures
We investigated whether subtle modifications to the original
recovery logic could successfully mitigate recovery failures.
Our experiments indicated that workarounds exist for 14 out
of the 20 issues examined (SL1, SL2, SL3, HF2, HF4, HF5,
CS1, CS2, HB3, HB4, YN1, YN2, YN3, YN4), enabling
11

## Page 12

Conference’17, July 2017, Washington, DC, USA Submission # XXX
Issue AutoPilot A/B Test-
ing
Built-in
Preview
Vicious
Cycle [90]
Validation
Harness [81]
SL1 0.14s 0.13s 0.11s ✗ 15.72s
SL2 0.17s+TO 0.16s+TO ✗ ✗ ✗
SL3 ✗ ✗ ✗ ✗ ✗
HF1 1.31s ✗ ✗ ✗ ✗
HF2 1.53s ✗ ✗ ✗ ✗
HF3 ✗ ✗ ✗ ✗ ✗
HF4 53.89s ✗ ✗ ✗ ✗
HF5 6.60s ✗ ✗ ✗ ✗
CS1 223.73s ND ✗ ✗ ✗
CS2 71.30s ✗ ✗ ✗ ✗
CS3 1.00s+TO ND ✓0.98s+TO ✗ ✗
CS4 1.27s+TO ND ✓1.24s+TO ✗ ✗
HB1 1.31s ✗ ✗ ✗ ✗
HB2 ✗ ✗ ✗ ✗ ✗
HB3 13.22s ND+Cas. ✗ ✓ 14.65 ✗
HB4 12.58s ✗ ✗ ✓ 14.97s 30.01s
YN1 46.93s ✗ ✗ ✗ ✗
YN2 2.52s ✗ ✗ ✗ ✗
YN3 3.93s ND ✗ ✗ 9.76s
YN4 2.67s ND ✗ ✗ 9.17ss
Table 6. Detection results on 20 real-world recovery failures. ND =
Non-deterministic results; TO = Timeout; Cas. = Cascading Failure;
[TODO: We may add sth. to show those baselines are not fully
isolated with original environment]
Issue Buggy Ver. Correct Ver.
Base ❶ Pilot ❷ Base ❸ Pilot ❹ B+P ❺
SL1 0.13s 0.14s 18.64s 19.97s 21.27s
SL2 0.16s+TO 0.17s+TO 20.64s 22.35s 24.03s
SL3 Undetect. Undetect. 11.08s 12.10s 13.98s
HF1 1.27s 1.31s 1.65s 1.75s 2.70s
HF2 1.47s 1.53s 1.91s 2.00s 3.69s
HF3 Undetect. Undetect. 0.01 0.01 0.01
HF4 52.77s 53.89s 54.06s 55.88s 57.24s
HF5 6.55s 6.60s 8.57s 9.43s 10.63s
CS1 215.94s 223.73s 234.55s 245.98s 269.65s
CS2 68.24s 71.30s 258.59s 272.85s 301.81s
CS3 0.98s 1.00s 161.74s 169.85s 186.94s
CS4 1.24s 1.27s 180.91s 191.56s 204.70s
HB1 1.09s 1.31s 1.74s 2.08s 3.35s
HB2 Undetect. Undetect. 18.93s 20.14s 23.57s
HB3 12.98s 13.22s 14.62s 15.86s 18.83s
HB4 12.03s 12.58s Unavail. Unavail. Unavail.
YN1 44.00s 46.93s 0.602s 1.237s 1.45s+50s
YN2 2.49s 2.52s 3.71s 4.02s 5.37s
YN3 3.86s 3.93s 6.66s 7.95s 9.88
YN4 2.56s 2.67s 6.26s 7.69s 9.44s
Table 7. Recovery time (seconds) under different configurations.
recovery to proceed safely without introducing further prob-
lems. Those workarounds include (1) using different options/-
parameters of the recovery to avoid the buggy recovery path,
(2)delaying or scheduling recovery to avoid race conditions
and resource conflicts and (3)throttling recovery operations to
prevent resource exhaustion and cascading failures (4)clean-
ing up problematic persistent data to enable correct recover.
[Maybe we need to compress those concrete examples]
HB3. A RegionServer crash was caused by an empty but
corrupted W AL file. Upon detection, HMaster initiated failover,
transferring the failed RegionServer’s responsibilities to oth-
ers. However, since the corrupted W AL remained untouched,
each recovery attempt triggered a NullPointerException(NPE),
cascading across the cluster and eventually crashing all Re-
gionServers. PILOT intercepts this NPE during pilot execution
and replaces the dangerous Runtime.halt() call, which is in-
voked when NPE is thrown, with a safe reporting API of
PILOT runtime lib. By flagging the faulty W AL file early,PI-
LOT enables operators to intervene—specifically, by deleting
the empty file—allowing recovery to proceed cleanly without
further data loss or crashes.
CS2. The recovery process requires each node to construct
and transmit MerkleTrees to the coordinator node to fix data
inconsistency. When inconsistencies are substantial, these
MerkleTrees can become excessively large, leading to Out-
OfMemoryError crashes during recovery. Using pilot execu-
tion, PILOT successfully anticipates and reports this failure
condition before it manifests. Based on insights from the pi-
lot run, developers could introduce practical mitigations to
reduce memory pressure: (1) subrange repairs, which divide
token ranges into smaller segments, and (2) table level repairs,
which scope the repair operation to individual tables rather
than entire keyspaces. Both strategies significantly reduce
MerkleTree size and prevent OOM conditions.
YN1. The system encounters a timing-sensitive vulnera-
bility during Resource Manager (RM) failover. If the RM
is switched over when a MapReduce job is being executed,
the FairScheduler of RM may attempt to access an empty
internal list used to denote containers’ scheduler keys dur-
ing container reassignment for failover, resulting in a No-
SuchElementException that crashes the newly recovered RM.
PILOT detects this subtle timing-related failure by simulating
the recovery path and observing the unsafe condition. As a
workaround, administrators can delay RM failover until the
MapReduce job fully completes, thus avoiding this critical
interval. With pilot execution, such issues are surfaced in
advance and help adjusting the recovery plan in time.
6.5 Exposing A New Recovery Bug
[Compress the content]
PILOT is designed as a runtime testing tool instead of a
bug finding technique. Nevertheless, in our experiments it
helps to expose a new recovery bug in the latest version of
HBase. In HBase, when a Scan/Get RPC attempts to allo-
cate an excessively large array, the request can trigger an
Out-Of-Memory (OOM) error on the server node. Developers
added an array size check that throws a DoNotRetryException
to prevent client retries, since retrying as a type of mitiga-
tion not only cannot make the request successful but would
also cause the OOM to propagate to other servers. However,
when mutating the inputs, PILOT occasionally reported er-
rors after pilot runs. Initially, we suspected this was a false
12

## Page 13

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
Sampled from eval Cassandra HDFS HBase YARN Solr
Y 99.61% 57.82% 92.61% 96.53% 96.21%
N 100% 99.75% 100% 94.77% 99.92%
Table 8. Tree edit distance similarity between pilot execution and
normal recovery.
System Analysis Time Generation Time
Solr 75s 115s
HDFS 47s 94s
Cassandra 51s 82s
HBase 63s 179s
Y ARN 92s 120s
Table 9. Static performance of PILOT .
positive—while PILOT performs pilot runs for retry-type re-
covery, retries should never be triggered in this scenario since
DoNotRetryException explicitly prevents them. Upon investi-
gation, we discovered that when the reservoir configuration
is disabled, the DoNotRetryException fails to propagate to
the client side, resulting in endless retry loops. We confirmed
this issue persists in the latest HBase branches. Our proposed
fix [14] has been confirmed by the developers in just a few
hours and merged into the master branch.
6.6 Accuracy of Pilot Run
[Need to polish] To evaluate the fidelity of pilot execution,
we construct execution trees for both pilot and normal recov-
ery paths based on our context tracking design (Section X.X).
We employ the Tree Edit Distance algorithm [54, 73], a stan-
dard metric for trace comparison, normalized by the original
execution tree’s node count to compute similarity scores. We
sample two recovery scenarios per system: one from our eval-
uated failures (Table 5) and another from automatically iden-
tified recovery points. The HDFS datanode recovery exhibits
lower similarity (57.82%) because some parts of the recov-
ery are triggered through implicit state interactions beyond
our tracking scope, and pilot execution excludes these parts.
The remaining divergences stem from three sources: non-
deterministic operations (e.g., random number generation),
time-sensitive functions affected by pilot-induced delays, and
concurrent state modifications that occur after pilot execution
creates its shadow version—any subsequent modifications by
original threads remain invisible to the pilot execution.
6.7 Performance and Overhead
Offline Performance We measure the performance of each
step in PILOT ’s workflow. Table 4 and Table 9 summarize
the static analysis results, including the time to identify pilot
entry points and instrumented threads, as well as the number
of such entry points and threads.
Online Setup [I update] We evaluated PILOT runtime over-too
long,
need
to
com-
press
head under two scenarios using standard benchmarks. First,
we measured overhead during normal operation without fault
injection. Second, we injected faults to trigger pilot execution
System Without Fault With Fault
w/o Pilot w/ Pilot w/o Pilot w/ Pilot
Solr 2135 2108 1960 1894
HDFS 156 147 101-150 93-147
Cassandra 31874 31652 27526 25496
HBase 21527 21455
Y ARN
Table 10. System throughput under different configurations. [Add
new systems]
System Without Fault With Fault
w/o Pilot w/ Pilot w/o Pilot w/ Pilot
Solr 1999MB 2007MB 2579MB 2632MB
HDFS 263MB 270MB 218MB-248MB 221MB-263MB
Cassandra 2431MB 2512MB 2174MB 2386MB
HBase 248MB 253MB
Y ARN
Table 11. System memory overhead under different configurations.
[Add new systems]
System Without Fault With Fault
w/o Pilot w/ Pilot w/o Pilot w/ Pilot
Solr 122% 127% 206% 220%
HDFS 44% 46% 47% 50%
Cassandra 274% 273% 341% 370%
HBase 81% 81%
Y ARN
Table 12. System cpu overhead under different configurations. [Add
new systems]
for recovery reactions to these faults. The faults we injected in-
clude: killing nodes, corrupting files, and network partitioning.
For network partitioning, we relied on Jepsen [26], a widely
used testing framework for distributed systems. We imple-
mented clients in Clojure for all evaluated systems and defined
common APIs. Jepsen automatically injects network faults
every 30 seconds. The benchmarks used were: YCSB for Cas-
sandra/HBase (40 clients, 100K requests, 50% reads), DFSIO
for YARN (400 files of 10MB each), the built-in NNBench-
WithoutMR for HDFS (which creates and writes 100 files,
with each file containing 160 blocks of 1MB each), and
Apache JMeter for Solr (600K search queries, 300 clients).
Online Results Table 10 summarizes the results. When pi-
lot execution is not triggered, PILOT incurs negligible over-
head (0.7%–1.1%). When pilot execution is triggered, the
system experiences moderate overhead (8.3%–13.9%) due
to deferred recovery and context propagation. [Add memory
data]
6.8 False Alarms
False Positive We evaluated the false positive rate ofPILOT
under moderate workloads (Section 6.7). The observed rates
are: Cassandra (0%), HBase (TODO%), HDFS (TODO%),
YARN (TODO%), and Solr (0.3%). Overall, PILOT incurs
a low false alarm rate, primarily because it captures explicit
13

## Page 14

Conference’17, July 2017, Washington, DC, USA Submission # XXX
error signals that reliably indicate buggy recovery behavior.
The remaining false positives occur when pilot execution con-
servatively reports failures that production recovery would tol-
erate—for example, flagging transient exceptions that would
succeed after retries in the real system.
False Negative While PILOT propagates PilotContext to
trace recovery behaviors, it may still miss latent or deferred
effects that manifest only under specific post-recovery event
sequences. In such cases, pilot execution may modify system
state in a faulty manner without triggering any immediate
error. However, subsequent normal operations, can surface
the bug, making it undetectable during the pilot execution.
HB-2 in Table 5 falls into this category: the recovery process
for the dead region server completes successfully, but the
failure only manifests when a client-side request arrives—an
event outside the recovery logic and beyond the scope of pilot
execution. As a result, PILOT incorrectly marks this faulty
recovery path as safe.
7 Limitations and Future Work
We discuss limitations with our approach. First, fully captur-
ing and modeling all the interactions is inherently complex
for production systems. PILOT ’s context propagation is im-
perfect: e.g., a skipped lease renewal message may trigger
cascading changes that are hard to track. Subtle performance
shifts also complicate modeling. We plan to extend support
for richer system dynamics. Second, concurrency also poses
challenges. PILOT uses speculative lock to handle pilot and
non-pilot interleavings, but nondeterministic failures remain
hard to reproduce. One direction is to leverage pilot traces to
enforce deterministic interleavings. Finally, choosing effec-
tive recovery strategies remains an open problem. We envision
integrating LLMs and agents to interpret structured pilot out-
puts, propose candidate plans, and iteratively validate them
in the sandbox, enabling more adaptive recovery.
8 Related Work
Failure recovery in distributed systems is well-studied [ 50,
51, 56, 66, 67, 85, 86], yet many techniques treat failures in
isolation and overlook cross-component interactions, a major
source of recovery bugs [43, 77, 80]. Prior work categorizes
recovery misbehaviors observed in production [58] and high-
lights common causes—metastability under overload [ 62],
vicious cycles from unbounded retry [89, 95]. In contrast, we
examine diverse failure patterns and their cross-component
interactions rather than a single mechanism.
A line of work models distributed system dependency to
understand correlated impacts bought by system changes/up-
dates. INDaaS [101] and CloudCanary [100] construct fault
graphs from dependency data and performs audits to prevent
correlated failures. Some works [46, 49, 55] formally verify
that network properties still hold after configuration changes.
Our methodology is primarily empirical and complements
these existing efforts.
A/B testing is a popular approach to assess recovery ef-
fects without risking the whole cluster [65, 81]. NetPilot [98]
addresses failures in datacenter networks by iterating candi-
date devices and applying mitigation. Narya [68] averts VM
failures by experimenting with different mitigation actions to
discover optimal actions. A/B testing has two key limitations:
its results may not generalize across heterogeneous nodes and
workloads, and correlated or cascading failures can propagate
beyond the test slice.
Several systems mask errors after they occur: failure-oblivious
computing [92] discards invalid writes and fabricates return
values to keep execution going; Rx [ 91] rolls back to a re-
cent checkpoint and re-executes under modified conditions;
Shadow Filesystem [72] redirects execution to a verified sys-
tem implementation during faults. These techniques mitigate
symptoms post hoc but do not surface recovery hazards early.
In contrast, we aim to expose such issues beforehand, before
they impact production.
Speculative execution pre-computes work to hide latency
and improve performance, originating in for processors [47,
61, 70, 83, 87] and later adapted to software systems [53, 69,
71, 82]. Examples include Speculator [83], which continues
execution while remote I/O is pending, and Xsyncfs [ 84],
which optimizes synchronous I/O in local file systems by
proactively deferring output until commit. They have distinct
goals and challenges as our approach focuses on improving
reliability rather than performance.
9 Conclusion
As cloud systems become increasingly complex, correctly
recovering systems from failures requires a more rigorous
approach. In this work we first present a study of real-world
recovery failures in popular distributed systems. Based on
the finding, we introduce pilot execution, a method to vali-
date failure recovery consequences before applying them to
production systems. We present PILOT , which automatically
enables pilot execution for large systems software. Our eval-
uation results show that PILOT is effective and efficient for
real-world distributed systems. chang: TODO: 2) finish 4.7 3)
compress the design section to 4-5pages 4) polish eval section
5) refine section 3 2) clarify the meta question (scope, usage)
3) ensure all SOSP review feedbacks are addressed 4) reflect
what are some missing issues not addressed yet (read orbit,
pivot tracing to identify missing questions)
References
[1] Apache ZooKeeper releases. https://zookeeper.apache.org/releases.
html.
[2] CASSANDRA-13938: Default repair is broken, crashes other nodes
participating in repair (in trunk). https://issues.apache.org/jira/
browse/CASSANDRA-13938.
[3] CASSANDRA-14096: Cassandra 3.11.1 repair causes out of memory.
https://issues.apache.org/jira/browse/CASSANDRA-14096.
[4] CASSANDRA-6415: Snapshot repair blocks for ever if something
happens to the "i made my snapshot" response. https://issues.apache.
14

## Page 15

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
org/jira/browse/CASSANDRA-6415.
[5] CASSANDRA-7560: ’nodetool repair -pr’ leads to indefinitely
hanging antientropysession. https://issues.apache.org/jira/browse/
CASSANDRA-7560.
[6] CASSANDRA: nodetool repair. https://cassandra.apache.org/doc/4.
0/cassandra/operating/repair.html.
[7] Configuring failure detection in zookeeper. https://www.ibm.com/
docs/en/b2b-integrator/5.2?topic=zookeeper-configuring-failure-
detection-in.
[8] HBASE-12770: Don’t transfer all the queued hlogs of a dead server to
the same alive server. https://issues.apache.org/jira/browse/HBASE-
12770.
[9] HBASE-13567: [dlr] region stuck in recovering mode. https://issues.
apache.org/jira/browse/HBASE-13567.
[10] HBASE-13877: Interrupt to flush from tableflushprocedure causes
dataloss in itbll. https://issues.apache.org/jira/browse/HBASE-13877.
[11] HBASE-14598: Bytebufferoutputstream grows its heapbytebuffer be-
yond jvm limitations. https://issues.apache.org/jira/browse/HBASE-
14598.
[12] HBASE-25898: Rs getting aborted due to npe in replication walen-
trystream. https://issues.apache.org/jira/browse/HBASE-25898.
[13] HBASE-9737: Corrupt hfile cause resource leak leading to region
server oom. https://issues.apache.org/jira/browse/HBASE-9737.
[14] HBASE-XXXXX: Anonymized for submission.
[15] HBSE-19980: Nullpointerexception when restoring a snapshot af-
ter splitting a region. https://issues.apache.org/jira/browse/HBASE-
19980.
[16] HDFS-10320: Rack failures may result in nn terminate. https://issues.
apache.org/jira/browse/HDFS-10320.
[17] HDFS-12070: Failed block recovery leaves files open indefinitely and
at risk for data loss. https://issues.apache.org/jira/browse/HDFS-
12070.
[18] HDFS-12914: Block report leases cause missing blocks until next
report. https://issues.apache.org/jira/browse/HDFS-12914.
[19] HDFS-14459: Closedchannelexception silently ignored in fsvol-
umelist.addblockpool(). https://issues.apache.org/jira/browse/HDFS-
14459.
[20] HDFS-15957: The ignored ioexception in the rpc response sent by
fseditlogasync can cause the hdfs client to hang. https://issues.apache.
org/jira/browse/HDFS-15957.
[21] HDFS-16115: Asynchronously handle bpserviceactor command mech-
anism may result in bpserviceactor never fails even commandprocess-
ingthread is closed with fatal error. https://issues.apache.org/jira/
browse/HDFS-16115.
[22] HDFS-16689: Standby namenode crashes when transitioning to active
with in-progress tailer. https://issues.apache.org/jira/browse/HDFS-
16689.
[23] HDFS-4937: Replicationmonitor can infinite-loop in blockplacement-
policydefault#chooserandom(). https://issues.apache.org/jira/browse/
HDFS-4937.
[24] HDFS-9908: Datanode should tolerate disk scan failure during nn
handshake. https://issues.apache.org/jira/browse/HDFS-9908.
[25] Java cloning library. https://github.com/kostaskougios/cloning.
[26] Jepsen: Distributed systems safety research. https://jepsen.io/.
[27] KAFKA-10101: recovery point is advanced without flushing the data
after recovery. https://issues.apache.org/jira/browse/KAFKA-10101.
[28] KAFKA-10832: Recovery logic is using incorrect producerstateman-
ager instance when updating producers. https://issues.apache.org/
jira/browse/KAFKA-10832.
[29] KAFKA-13600: Rebalances while streams is in degraded state can
cause stores to be reassigned and restore from scratch. https://issues.
apache.org/jira/browse/KAFKA-13600.
[30] Kip-537: Increase default zookeeper session timeout.
https://cwiki.apache.org/confluence/display/KAFKA/KIP-
537%3A+Increase+default+zookeeper+session+timeout.
[31] MESOS-6270: Agent crashes when trying to recover pods.. https:
//issues.apache.org/jira/browse/MESOS-6270.
[32] Nodes and ephemeral nodes - apache zookeeper. https://zookeeper.
apache.org/doc/r3.4.6/zookeeperOver.html.
[33] OpenTelemetry: High-quality, ubiquitous, and portable telemetry to
enable effective observability. https://opentelemetry.io/.
[34] RABBITMQ-658: [ocf ha] do not check cluster health if master is not
elected. https://github.com/rabbitmq/rabbitmq-server/pull/658.
[35] SOLR-10914: Recoverystrategy’s sendpreprecoverycmd can get stuck
for 5 minutes if leader is unloaded. https://issues.apache.org/jira/
browse/SOLR-10914.
[36] SOLR-17515: Recovery fails in solr 9.7.0 if basic-auth is enabled.
https://issues.apache.org/jira/browse/SOLR-17515.
[37] SOLR-6056: Zookeeper crash jvm stack oom because of recover
strategy. https://issues.apache.org/jira/browse/SOLR-6056.
[38] TiDB-963: Tikv cluster not respecting crd replica configuration. https:
//github.com/pingcap/tidb-operator/issues/963.
[39] YARN-2816: Nm fail to start with npe during container recovery.
https://issues.apache.org/jira/browse/YARN-2816.
[40] YARN-4347: Resource manager fails with null pointer exception.
https://issues.apache.org/jira/browse/YARN-4347.
[41] YARN-6403: Invalid local resource request can raise npe and make
nm exit. https://issues.apache.org/jira/browse/YARN-6403.
[42] Y ARN-7382: Nosuchelementexception in fairscheduler after failover
causes rm crash. https://issues.apache.org/jira/browse/YARN-7382.
[43] R. Alagappan, A. Ganesan, E. Lee, A. Albarghouthi, V . Chidambaram,
A. C. Arpaci-Dusseau, and R. H. Arpaci-Dusseau. Protocol-Aware
recovery for Consensus-Based storage. In 16th USENIX Conference
on File and Storage Technologies (FAST 18), pages 15–32. USENIX
Association, Feb. 2018.
[44] Amazon. Aws dynamodb service event in the us-east region. https:
//aws.amazon.com/cn/message/5467D2/.
[45] A. Baumann, J. Appavoo, O. Krieger, and T. Roscoe. A fork () in
the road. In Proceedings of the workshop on hot topics in operating
systems, pages 14–22, 2019.
[46] R. Beckett, A. Gupta, R. Mahajan, and D. Walker. A general approach
to network configuration verification. In Proceedings of the Confer-
ence of the ACM Special Interest Group on Data Communication ,
SIGCOMM ’17, page 155–168, Los Angeles, CA, USA, 2017.
[47] P. Bernstein, S. Bykov, A. Geller, G. Kliot, and J. Thelin. Orleans: Dis-
tributed virtual actors for programmability and scalability. Technical
Report MSR-TR-2014-41, March 2014.
[48] C. Breck. Kubernetes liveness and readiness probes: How to avoid
shooting yourself in the foot. https://blog.colinbreck.com/kubernetes-
liveness-and-readiness-probes-how-to-avoid-shooting-yourself-
in-the-foot/ .
[49] M. Brown, A. Fogel, D. Halperin, V . Heorhiadi, R. Mahajan, and
T. Millstein. Lessons from the evolution of the batfish configuration
analysis tool. In Proceedings of the ACM SIGCOMM 2023 Conference,
ACM SIGCOMM ’23, page 122–135, New York, NY , USA, 2023.
[50] G. Candea, S. Kawamoto, Y . Fujiki, G. Friedman, and A. Fox. Mi-
croreboot — a technique for cheap recovery. In Proceedings of the
6th Conference on Symposium on Operating Systems Design & Imple-
mentation - Volume 6, OSDI’04, page 3, San Francisco, CA, 2004.
[51] K. M. Chandy and L. Lamport. Distributed snapshots: Determin-
ing global states of distributed systems. ACM Trans. Comput. Syst.,
3(1):63–75, Feb. 1985.
[52] M. D. Ernst, J. H. Perkins, P. J. Guo, S. McCamant, C. Pacheco, M. S.
Tschantz, and C. Xiao. The daikon system for dynamic detection of
likely invariants. Sci. Comput. Program., 69(1–3):35–45, Dec. 2007.
[53] A. Estebanez, D. R. Llanos, and A. Gonzalez-Escribano. A survey on
thread-level speculation techniques. ACM Comput. Surv., 49(2), June
2016.
15

## Page 16

Conference’17, July 2017, Washington, DC, USA Submission # XXX
[54] Z. Fan, X. Gao, M. Mirchev, A. Roychoudhury, and S. H. Tan. Au-
tomated repair of programs from large language models. In 2023
IEEE/ACM 45th International Conference on Software Engineering
(ICSE), pages 1469–1481. IEEE, 2023.
[55] A. Fogel, S. Fung, L. Pedrosa, M. Walraed-Sullivan, R. Govindan,
R. Mahajan, and T. Millstein. A general approach to network configu-
ration analysis. In 12th USENIX Symposium on Networked Systems
Design and Implementation (NSDI 15) , pages 469–483. USENIX
Association, May 2015.
[56] A. Ganesan, R. Alagappan, A. C. Arpaci-Dusseau, and R. H. Arpaci-
Dusseau. Redundancy does not imply fault tolerance: Analysis of
distributed storage reactions to single errors and corruptions. In 15th
USENIX Conference on File and Storage Technologies (FAST 17) ,
pages 149–166. USENIX Association, Feb. 2017.
[57] H. S. Gunawi, C. Rubio-González, A. C. Arpaci-Dusseau, R. H.
Arpaci-Dussea, and B. Liblit. EIO: Error handling is occasionally
correct. In Proceedings of the 6th USENIX Conference on File and
Storage Technologies, FAST ’08, pages 14:1–14:16, San Jose, Califor-
nia, 2008.
[58] Z. Guo, S. McDirmid, M. Yang, L. Zhuang, P. Zhang, Y . Luo,
T. Bergan, P. Bodik, M. Musuvathi, Z. Zhang, and L. Zhou. Fail-
ure recovery: When the cure is worse than the disease. In Proceedings
of the 14th USENIX Conference on Hot Topics in Operating Systems,
HotOS’13, pages 8–8, Santa Ana Pueblo, New Mexcio, 2013.
[59] Helius. A complete history of solana outages: Causes, fixes,
and lessons learnt. https://www.helius.dev/blog/solana-outages-
complete-history.
[60] B. Holland, G. R. Santhanam, and S. Kothari. Transferring state-of-
the-art immutability analyses: Experimentation toolbox and accuracy
benchmark. In IEEE International Conference on Software Testing,
Verification and Validation, ICST ’17, pages 484–491, March 2017.
[61] G. Hu, A. Arpaci-Dusseau, and R. Arpaci-Dusseau. Foreactor: Ex-
ploiting storage i/o parallelism with explicit speculation, 2024.
[62] L. Huang, M. Magnusson, A. B. Muralikrishna, S. Estyak, R. Isaacs,
A. Aghayev, T. Zhu, and A. Charapko. Metastable failures in the
wild. In 16th USENIX Symposium on Operating Systems Design and
Implementation (OSDI 22), pages 73–90, 2022.
[63] P. Huang, C. Guo, L. Zhou, J. R. Lorch, Y . Dang, M. Chintalapati,
and R. Yao. Gray failure: The Achilles’ heel of cloud-scale systems.
In Proceedings of the 16th Workshop on Hot Topics in Operating
Systems, HotOS XVI. ACM, May 2017.
[64] W. Huang, A. Milanova, W. Dietl, and M. D. Ernst. Reim & ReIm-
Infer: Checking and inference of reference immutability and method
purity. In Proceedings of the ACM International Conference on Ob-
ject Oriented Programming Systems Languages and Applications ,
OOPSLA ’12, pages 879–896, Tucson, Arizona, USA, 2012.
[65] R. Kohavi and S. Thomke. The surprising power of online experiments.
Harvard business review, 95(5):74–82, 2017.
[66] R. Koo and S. Toueg. Checkpointing and rollback-recovery for dis-
tributed systems. In Proceedings of 1986 ACM Fall Joint Computer
Conference, ACM ’86, page 1150–1158, Dallas, Texas, USA, 1986.
[67] L. Lamport. Paxos made simple. ACM Sigact News, 32(4):18–25,
2001.
[68] S. Levy, R. Yao, Y . Wu, Y . Dang, P. Huang, Z. Mu, P. Zhao, T. Ramani,
N. Govindraju, X. Li, Q. Lin, G. L. Shafriri, and M. Chintalapati.
Predictive and adaptive failure mitigation to avert production cloud
vm interruptions. In Proceedings of the 14th USENIX Symposium on
Operating Systems Design and Implementation, OSDI ’20. USENIX,
November 2020.
[69] N. Li, A. Kalaba, M. J. Freedman, W. Lloyd, and A. Levy. Speculative
recovery: Cheap, highly available fault tolerance with disaggregated
storage. In 2022 USENIX Annual Technical Conference (USENIX
ATC 22), pages 271–286. USENIX Association, July 2022.
[70] S. S. Liao, P. H. Wang, H. Wang, G. Hoflehner, D. Lavery, and J. P.
Shen. Post-pass binary adaptation for software-based speculative pre-
computation. In Proceedings of the ACM SIGPLAN 2002 Conference
on Programming Language Design and Implementation, PLDI ’02,
page 117–128, Berlin, Germany, 2002.
[71] G. Liargkovas, K. Kallas, M. Greenberg, and N. Vasilakis. Executing
shell scripts in the wrong order, correctly. In Proceedings of the 19th
Workshop on Hot Topics in Operating Systems , HOTOS ’23, page
103–109, Providence, RI, USA, 2023.
[72] J. Liu, X. Hao, A. Arpaci-Dusseau, R. Arpaci-Dusseau, and T. Chajed.
Shadow filesystems: Recovering from filesystem runtime errors via
robust alternative execution. In Proceedings of the 16th ACM Work-
shop on Hot Topics in Storage and File Systems, HotStorage ’24, page
15–22, Santa Clara, CA, USA, 2024.
[73] J. Liu, C. S. Xia, Y . Wang, and L. Zhang. Is your code generated by
chatgpt really correct? rigorous evaluation of large language models
for code generation. Advances in Neural Information Processing
Systems, 36, 2024.
[74] X. Liu, Z. Guo, X. Wang, F. Chen, X. Lian, J. Tang, M. Wu, M. F.
Kaashoek, and Z. Zhang. D3s: Debugging deployed distributed sys-
tems. In Proceedings of the 5th USENIX Symposium on Networked Sys-
tems Design and Implementation, NSDI ’08, page 423–437. USENIX
Association, 2008.
[75] C. Lou, P. Huang, and S. Smith. Understanding, detecting and lo-
calizing partial failures in large system software. In 17th USENIX
Symposium on Networked Systems Design and Implementation, NSDI
’20, pages 559–574. USENIX Association, Feb. 2020.
[76] D. E. Lowell, S. Chandra, and P. Chen. Exploring failure transparency
and the limits of generic recovery. In Fourth Symposium on Oper-
ating Systems Design and Implementation (OSDI 2000) . USENIX
Association, Oct. 2000.
[77] J. Lu, C. Liu, L. Li, X. Feng, F. Tan, J. Yang, and L. You. Crashtuner:
detecting crash-recovery bugs in cloud systems via meta-info analysis.
In Proceedings of the 27th ACM Symposium on Operating Systems
Principles, SOSP ’19, page 114–130, Huntsville, Ontario, Canada,
2019.
[78] J. Mace, P. Bodik, R. Fonseca, and M. Musuvathi. Retro: Targeted
resource management in multi-tenant distributed systems. In Proceed-
ings of the 12th USENIX Conference on Networked Systems Design
and Implementation, NSDI’15, page 589–603, Oakland, CA, 2015.
[79] J. Mace, R. Roelke, and R. Fonseca. Pivot tracing: dynamic causal
monitoring for distributed systems. In Proceedings of the 25th Sym-
posium on Operating Systems Principles, SOSP ’15, page 378–393,
Monterey, California, 2015.
[80] P. D. Marinescu and G. Candea. Efficient testing of recovery code
using fault injection. ACM Trans. Comput. Syst., 29(4), Dec. 2011.
[81] K. Nagaraja, F. Oliveira, R. Bianchini, R. P. Martin, and T. D. Nguyen.
Understanding and dealing with operator mistakes in internet services.
In 6th Symposium on Operating Systems Design & Implementation
(OSDI 04). USENIX Association, Dec. 2004.
[82] R. Netravali and J. Mickens. Reverb: Speculative debugging for
web applications. In Proceedings of the ACM Symposium on Cloud
Computing, SoCC ’19, page 428–440, Santa Cruz, CA, USA, 2019.
[83] E. B. Nightingale, P. M. Chen, and J. Flinn. Speculative execution in
a distributed file system. In Proceedings of the Twentieth ACM Sym-
posium on Operating Systems Principles, SOSP ’05, page 191–205,
Brighton, United Kingdom, 2005.
[84] E. B. Nightingale, K. Veeraraghavan, P. M. Chen, and J. Flinn. Re-
think the sync. In Proceedings of the 7th Symposium on Operating
Systems Design and Implementation, OSDI ’06, page 1–14, Seattle,
Washington, 2006.
[85] D. Ongaro and J. Ousterhout. In search of an understandable con-
sensus algorithm. In Proceedings of the 2014 USENIX Conference
on USENIX Annual Technical Conference, USENIX ATC’14, page
16

## Page 17

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
305–320, Philadelphia, PA, 2014.
[86] J. Ousterhout, A. Gopalan, A. Gupta, A. Kejriwal, C. Lee, B. Mon-
tazeri, D. Ongaro, S. J. Park, H. Qin, M. Rosenblum, S. Rumble,
R. Stutsman, and S. Yang. The ramcloud storage system. ACM Trans.
Comput. Syst., 33(3), Aug. 2015.
[87] A. E. Papathanasiou and M. L. Scott. Aggressive prefetching: an idea
whose time has come. In Proceedings of the 10th Conference on Hot
Topics in Operating Systems - Volume 10, HOTOS’05, page 6, Santa
Fe, NM, 2005.
[88] Parse.ly. Kafkapocalypse: a postmortem on our service outage. https:
//www.parse.ly/kafkapocalypse/.
[89] S. Qian, W. Fan, L. Tan, and Y . Zhang. Vicious cycles in distributed
software systems. In 2023 38th IEEE/ACM International Conference
on Automated Software Engineering (ASE) , pages 91–103. IEEE,
2023.
[90] S. Qian, W. Fan, L. Tan, and Y . Zhang. Vicious cycles in distributed
software systems. In Proceedings of the 38th IEEE/ACM Interna-
tional Conference on Automated Software Engineering , ASE ’23,
page 91–103, Echternach, Luxembourg, 2024.
[91] F. Qin, J. Tucek, J. Sundaresan, and Y . Zhou. Rx: treating bugs as
allergies—a safe method to survive software failures. In Proceedings
of the Twentieth ACM Symposium on Operating Systems Principles,
SOSP ’05, page 235–248, Brighton, United Kingdom, 2005.
[92] M. Rinard, C. Cadar, D. Dumitran, D. M. Roy, T. Leu, and J. William
S. Beebee. Enhancing server availability and security through Failure-
Oblivious computing. In 6th Symposium on Operating Systems Design
& Implementation (OSDI 04). USENIX Association, Dec. 2004.
[93] Spotify. Incident management at spotify.https://engineering.atspotify.
com/2013/6/incident-management-at-spotify .
[94] Srcco. Liveness probes are dangerous. https://srcco.de/posts/
kubernetes-liveness-probes-are-dangerous.html .
[95] B. A. Stoica, U. Sethi, Y . Su, C. Zhou, S. Lu, J. Mace, M. Musuvathi,
and S. Nath. If at first you don’t succeed, try, try, again...? insights
and llm-informed tooling for detecting retry bugs in software systems.
In Proceedings of the ACM SIGOPS 30th Symposium on Operating
Systems Principles, SOSP ’24, page 63–78, Austin, TX, USA, 2024.
[96] TechInformed. Microsoft confirms ddos cyberattack behind sec-
ond outage. https://techinformed.com/microsoft-confirms-ddos-
cyberattack-behind-second-it-outage/ .
[97] R. Vallée-Rai, P. Co, E. Gagnon, L. Hendren, P. Lam, and V . Sundare-
san. Soot - a java bytecode optimization framework. In Proceedings
of the 1999 Conference of the Centre for Advanced Studies on Col-
laborative Research, CASCON ’99, page 13, Mississauga, Ontario,
Canada, 1999.
[98] X. Wu, D. Turner, C.-C. Chen, D. A. Maltz, X. Yang, L. Yuan, and
M. Zhang. Netpilot: automating datacenter network failure mitigation.
SIGCOMM Comput. Commun. Rev., 42(4):419–430, aug 2012.
[99] D. Yuan, Y . Luo, X. Zhuang, G. R. Rodrigues, X. Zhao, Y . Zhang, P. U.
Jain, and M. Stumm. Simple testing can prevent most critical failures:
An analysis of production failures in distributed data-intensive systems.
In Proceedings of the 11th USENIX Conference on Operating Systems
Design and Implementation, OSDI’14, pages 249–265, Broomfield,
CO, 2014.
[100] E. Zhai, A. Chen, R. Piskac, M. Balakrishnan, B. Tian, B. Song, and
H. Zhang. Check before you change: Preventing correlated failures in
service updates. In 17th USENIX Symposium on Networked Systems
Design and Implementation (NSDI 20) , pages 575–589. USENIX
Association, Feb. 2020.
[101] E. Zhai, R. Chen, D. I. Wolinsky, and B. Ford. Heading off cor-
related failures through independence-as-a-service. In Proceedings
of the 11th USENIX Conference on Operating Systems Design and
Implementation, OSDI’14, page 317–334, Broomfield, CO, 2014.
Appendix A Automatically Enabling Pilot
Execution
Manually enabling pilot execution in existing software is
both time-consuming and error-prone, as it requires tailor-
ing the logic to specific software implementations. Moreover,
maintaining consistency with the original system after each
software update is challenging. To address these issues, we
developed PILOT , a static analysis tool designed to automati-
cally enable pilot execution for distributed systems.
Workflow chang: compress In the offline transformation
phase, PILOT analyzes source code S to identify recovery
entry points R through static analysis, focusing on patterns
that may lead to cross-thread or cross-process interactions.
It generates pilot-version functions F′ = {f ′
1, f ′
2,... } for each
application function in F = {f1, f2,... } (skipping excluded
infrastructure packages) and instruments each entry point
ri ∈ R to support conditional redirection to pilot mode. F′
are instrumented to enable context propagation across thread
and process boundaries to ensure comprehensive tracking of
recovery behavior and provides isolation mechanism.
In the runtime execution phase, when recovery triggers atri
with pilot mode enabled, the PILOT runtime library creates an
isolated execution context proactively using phantom threads
Tphantom = {t1,t2,... } and redirects flow through pilot-version
functions f ′
1, f ′
2,... . During pilot execution, the runtime li-
brary dynamically spawns additional phantom threads when-
ever original threads encounter pilot-marked state—effectively
"forking" execution at these interaction points to continue
pilot execution in isolation while leaving original threads
undisturbed. Upon completion, the runtime provides oper-
ators with execution feedback and safely cleans up all the
resources in pilot execution including phantom threads before
returning control to the original system. This design enables
operators to safely preview recovery behavior before com-
mitting to actual execution, significantly reducing the risk of
recovery-induced failures in production distributed systems.
Input and Output To apply PILOT on a new system, devel-
opers provide: (1) the system’s source code S, (2) a configura-
tion file specifying code paths, compilation instructions, and
self-implemented underlying communication packages P (if
any) to exclude from instrumentation (e.g., self-implemented
RPC frameworks), and (3) manual modifications to P to sup-
port global propagation of context
PILOT outputs: (1) an instrumented version S′ containing
transformed entry points for the candidates R, pilot-version
functions F′ for each application function with context prop-
agation instrumentation at interaction boundaries and multi-
level isolation mechanisms, and (2) a runtime library attached
to S′ for managing pilot execution.
17

## Page 18

Conference’17, July 2017, Washington, DC, USA Submission # XXX
A.1 Enabling accurate pilot execution
A.1.1 Bootstrap Pilot Execution chang: what is entry
points and why we need to identify them?
chang: what to do with entry points?
Identify Entry Points [I am not sure if this is the correct
definition for entry point] To accurately mimic recovery be-
havior, pilot execution should start from the same point where
recovery begins. Therefore, PILOT begins by identifying en-
try points of recovery—where recovery starts—through static
analysis. Based on Finding 2, recovery entry points fall into
two categories: passive and proactive. Passive handlers in-
clude error-handling constructs (e.g., try-catch blocks) and
listeners for third-party services (e.g., ZooKeeper). Proactive
handlers are typically implemented as CLI commands, such
as Cassandra’s nodetool repair, which follow well-defined
invocation patterns. Since both passive and proactive recovery
entry points often exhibit recognizable patterns, AUTOPILOT
identifies them using static analysis with predefined rules.
Please note not all code segments matching these patterns are
suitable for pilot execution, and indiscriminately instrument-
ing all of them could introduce significant runtime overhead.
Instead, AUTOPILOT focuses on code blocks likely to lead to
complex recovery failures with inter-thread or inter-process
interactions, as identified in Finding 5. Specifically, for all
the recovery entry points identified, AUTOPILOT performs
interprocedural analysis to determine whether they contain
invocations that may lead to cross-thread or cross-process
interactions (e.g., executor.submit()), and enables pilot exe-
cution for those entry points. We also provide function-level
annotation for operators—AUTOPILOT will automatically
apply the same instrumentation to the annotated functions
in case we miss some error-prone recovery entry points. In
Figure 7, we illustrate the recovery entry point for the motivat-
ing HBase example. The RegionServerTracker class, which
inherits from the ZooKeeper Listener class, implements the
nodeChildrenChanged function as a callback triggered when
listening for the event that a region server fails, initiating
recovery.
Instrument Entry Points Once an entry point is identi-
fied, PILOT instruments the code to divert execution into
pilot mode. As shown in Figure 7, the PILOT runtime li-
brary generates a globally unique pilot execution ID (an in-
crementing integer) and creates a PilotContext object via
PilotUtil.initNewExec. The PilotContext is implemented
as a thread-local map that stores pilot-related metadata, in-
cluding this ID, enabling per-thread access to pilot execution
state. Additional metadata stored in this context will be de-
scribed later. The globally unique ID is essential because
pilot executions may be triggered multiple times for different
recoveries, and the ID differentiates these rounds. PilotU-
til.initNewExec obtains this ID through ZooKeeper’s coordi-
nation service and registers it under the/pilot-id directory in
ZooKeeper. With the PilotContext initialized, PILOT inserts
Original 
implementation 
Pilot 
runtime 
AutoPilot 
Pilot implementation 
➊ analyze & 
instrument 
➋ generate ➌ install 
monitor 
Figure 6. PILOT workflow.
PilotUtil.execute(c.wrap(this::nodeChildrenChanged$pilot)),
which sets the PilotContext as the executing thread’s lo-
cal variable. Here, nodeChildrenChanged$pilot is a statically
generated pilot version of the original function—PILOT stati-
cally generates such pilot versions for all functions to ensure
proper isolation and context propagation. Finally, PilotU-
til.waitUntilFinished(c) waits for the pilot execution to
complete and performs global cleanup based on ZooKeeper,
as detailed in "Manage the lifecycle of phamtom threads".
chang: essentially you are talking about removing mis-
identified cases
chang: what if you miss some entry points or identify false
entry points?
A.1.2 Propagating Pilot Execution Globally with Con-
text The goal of context propagation is to let pilot execution
faithfully mimic the original recovery logic across threads
and processes, capturing all its effects without impacting
production state. AUTOPILOT firstly replaces synchronous
calls within each pilot-version function to ensure they exe-
cute in isolation for a single thread. However, modern dis-
tributed systems frequently execute recovery logic across
threads and processes. For example, in Cassandra, nodetool
repair is encapsulated in RepairJob tasks and dispatched to
thread pools. With only synchronous-call instrumentation,
these tasks—when executed in other threads—cannot detect
that they are part of a pilot execution, and thus run the original
recovery code instead of their pilot versions.
To address this, we catalog common inter-thread and inter-
process interaction patterns observed in our failure study
(Finding 5) and design a runtime context-propagation mecha-
nism inspired by prior work such as Pivot Tracing [79] and
Retro [78]. This mechanism propagates PilotContext across
thread and process boundaries, ensuring that all recovery
actions—regardless of where they execute—are redirected to
their pilot versions. This also lays the foundation for provid-
ing feedback to operator, as it enables comprehensive tracking
of all pilot-version function executions (see Section 4.XXX[I
plan to discuss how we construct the context tracking tree in
providing feedback to operators]). chang: don’t have to bring
up early, can wait to discuss later. nice to make a note though
Figure 5 illustrates the different types of propagation we
support:
chang: need to make it concise, summarize the key idea of
each level
18

## Page 19

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
Figure 7. Instrumenting entry points for pilot execution.
Inter-thread (❷) We identified three common patterns for
cross-thread interaction in distributed systems: task-executor
model, synchronization primitives, and shared variable moni-
toring. The key insight is that threads interact through shared
states within the same address space in those patterns, and
PILOT instrument those shared states to carry PilotContext,
enabling propagation across thread boundaries.
Task-Executor Model. For asynchronous tasks submit-
ted to executor threads (e.g., RepairJob in Cassandra), we
instrument task classes that implement standard interfaces
(Runnable, Future, Callable) by adding a PilotContext field.
When a task is submitted from a pilot function, PILOT instru-
ments it to carry the submitting thread’sPilotContext. PILOT
also instruments the task’s interface functions: if the Pilot-
Context contains a valid pilot ID, the task redirects to pilot-
version functions; otherwise, it executes normally. Therefore,
at runtime, if a task is created and submitted within a pilot
function, it will continue to redirect to pilot functions even
when executed in other threads. For custom task patterns (e.g.,
HBase’s recovery operations wrapped in a customized Proce-
dure class with self-implemented dedicated worker threads
using a queue-based SEDA design), we employ static data-
flow analysis from Panorama [ ? ] to identify such patterns
and ensure that tasks submitted in pilot mode execute with
dedicated pilot-aware worker threads that properly propagate
context (as detailed in Section 4.2).
Synchronization Primitives. PILOT runtime library pro-
vides wrapper versions for commonly used synchronization
primitives (e.g., ConditionVariable, CountDownLatch), which
attach additional data structures to track the relationship
among threads and enable context propagation. PILOT instru-
ments the code to replace these synchronization primitives
with their wrapper versions. For example, a condition vari-
able wrapper(Please refer to Algorithm 5) maintains a wait
queue recording all waiting threads. When a phantom thread
signals, the wrapper dequeues the next waiter: if it’s an origi-
nal thread, it triggers micro-fork with the phantom thread’s
PilotContext to create an isolated execution environment for
that thread to continue in pilot mode. The wrapper’s wait
queue serves as the bridge for context propagation—when
the phantom thread signals, it can propagate its PilotContext
through this data structure to simulate the pilot execution’s in-
fluence on original threads via newly created phantom threads
from micro-fork.
Shared Variable Monitoring. For cases where original
threads monitor variables that pilot execution might modify
(e.g., while(a>0){...} where a could be changed by pilot
execution), potentially affecting original thread execution, we
use static analysis to identify such shared variables—typically
those protected by locks or of concurrent types. These vari-
ables are augmented with a separatePilotContext field. When
pilot execution modifies such a variable, it marks the variable
with the currently executing pilot function’s thread’sPilot-
Context. We instrument the code by adding a conditional
statement before each access to the shared variable (e.g., if
(a.$pilotContext contains valid pilot ID) {redirect to
pilot function...}). When an original thread attempts to
access a variable marked with pilot context, this conditional
check detects the pilot modification and creates an isolated ex-
ecution environment for the affected code path (as described
in Section 4.2). While we cannot cover all such scenarios
due to their complexity, our static analysis focuses on simple,
identifiable patterns with clear data-flow dependencies and
concurrency markers.
Inter-process (❸) Cross-process propagation presents a dif-
ferent challenge than inter-thread communication: processes
lack shared state in the same address space for direct context
transfer. Our key insight is to serialize PilotContext at all
cross-process interaction points.
Communication Protocols (RPC/HTTP) At RPC and
HTTP send points, we serialize the PilotContext from the
sending thread into message headers. Popular RPC/HTTP li-
braries provide straightforward interceptor mechanisms—HTTP
frameworks offer .addHeader() methods and gRPC provides
metadata injection APIs—making instrumentation fully au-
tomatic. For systems with custom cross-process protocols
(e.g., HBase’s proprietary RPC framework), we extend their
serialization logic to include PilotContext with minimal ef-
fort, typically piggybacking on existing distributed tracing
code that already propagates metadata across processes. At
the receiving-side entry points, which are identifiable through
well defined interfaces (e.g., HTTP requests routed through
doFilter() interface, RPC interfaces defined in.proto files),
AUTO PILOT adds conditional logic: when a message contains
PilotContext in its header after deserialization, we refer to
PILOT runtime lib to create a dedicated thread to handle this
pilot-originating request. This thread inherits the PilotCon-
text from the serialized metadata in message header and
executes the pilot version of the handler functions.
This approach generalizes beyond RPC and HTTP to more
communication mechanisms by instrumenting send and re-
ceive endpoints. The underlying communication infrastruc-
ture remains unchanged—context propagation occurs trans-
parently through existing message channels.
19

## Page 20

Conference’17, July 2017, Washington, DC, USA Submission # XXX
Distributed Coordinaion Service For state update lis-
teners on third-party services ( ❸.b), PILOT propagates Pi-
lotContext by wrapping the system’s usage of third-party
client libraries with a proxy layer. The third-party service
remains unchanged—the proxy sits between the system code
and the third-party client library. Taking ZooKeeper as an
example, when a pilot function modify Zookeeper nodes
through Zookeeper client, PILOT replaces the client operation
with a wrapper, intercepts this call and performs additional
bookkeeping: it serializes the thread’sPilotContext to a meta-
data znode (e.g., /pilot/foo.pilot_context) . When a watch
event fires, the proxy intercepts the callback before it reaches
application code, retrieves the stored PilotContext from the
metadata znode, and creates a new thread with this context to
handle the event.
While our context propagation covers the common inter-
action patterns identified in our study (Finding 5), achiev-
ing complete tracking remains challenging. For example, al-
though we currently support ZooKeeper by abstracting its op-
erations into read/write interfaces with specialized handling
for watcher-triggered events, complex third-party services
may employ diverse communication patterns (e.g., custom
IPC, shared memory) that fall outside our instrumentation
scope. When encountering untrackable communication pat-
terns, we offer two strategies to ensure complete isolation
at the cost of reduced accuracy in pilot execution results.
The conservative approach replaces unhandled interactions
with PILOT runtime API calls to terminate pilot execution
by triggering the cleanup mechanisms in Section 4.x. The
permissive approach allows pilot execution to continue by
skipping uninstrumented operations, preserving broader sim-
ulation coverage while potentially missing certain recovery
actions.
20

## Page 21

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
A.2 Isolating Side Effects with Phantom Threads
[Add some highlights and motivation] Without proper iso-
lation, pilot execution can disrupt the production system in
three ways: First, exceptions thrown during pilot execution
may crash the original threads. Second, pilot execution may
modify production states in memory or on disk. Third, pilot
execution may delay original threads since executing pilot
version functions takes time.
A straightforward solution is to directly use fork() be-
fore pilot execution starts. However, as discussed in prior
work [45], fork() is heavyweight as it duplicates the entire
memory space, and the forked environment suffers from seri-
ous concurrency issues in distributed systems.
Instead, we implement fine-grained isolation specifically
for recovery-related execution. By leveraging the context
propagation mechanism from Section 4.1, we redirect pilot
execution to specialized pilot-version functions, which exe-
cute within a multi-layered sandbox (Figure 8) that provides:
(1) dedicated thread isolation, (2)shadow field redirection for
in-memory state modifications, (3) I/O interception that di-
verts file operations to isolated locations(4)third-party library
calls rerouted to isolated namespaces, and(5)neutralization of
dangerous system-level operations.
chang: at this paragraph, people typically expect some
highlights of what technique you will introduce and give a
summary of core ideas
A.2.1 Phantom Thread [One missing part is: how do we
prevent pilot execution from propagating endlessly? My idea
is: we already have PilotUtils.waitUntilFinished to manage
the execution time of pilot execution. Another metric to mea-
sure if pilot execution propagates endlessly is to track the
number of phantom threads currently alive (this is already
implemented through zookeeper). It is possible that pilot ex-
ecution could create tons of phantom threads, and that’s not
what we want. So, before each phantom thread is started, if
the number of phantom threads is above a threshold (maybe
simply configure this to 100), then we raise an alert and abort
pilot execution.]
Thread-level (❶) [I added explanation for what phantom
threads are] To achieve fault isolation while maintaining accu-
rate recovery simulation, PILOT redirects pilot execution from
original threads to a set of dedicated sidecar threads running
in the same address space, which we call phantom threads.
Unlike original threads, phantom threads will carryPilotCon-
text from the context propagation mechanism in section 4.1
and only execute pilot version functions, which never modify
the states in original system or acquire real locks that would
compete with production threads as described in 4.2.2. Each
phantom thread registers itself with ZooKeeper at startup and
deregisters at termination, enabling PILOT runtime library to
track all phantom threads associated with a specific pilot exe-
cution round and perform cleanup when needed (as detailed
in 4.2.2). Additionally, phantom threads are instrumented to
catch and report any exceptions or timeouts as evidence of
pilot execution failures, providing critical feedback for opera-
tors. chang: This subsection is about Phantom Thread, then
the first paragraph should be about Phantom Thread. You
did introduce how they run in the process, still, we need a
definition here. In other words, are phantom threads just a
dedicated thread pool that has nothing different compared
to ordinary threads? These phantom threads provide the first
layer of fault isolation—for example, if a phantom thread
crashes due to a null pointer exception during pilot execution,
the original thread remains intact and production operations
continue unaffected. We now explain how PILOT runtime
library creates and manages these phantom threads across
different interaction patterns.
Phantom Thread Creation. PILOT creates phantom threads
through two complementary approaches: proactive spawning
for predictable patterns and reactive spawning for dynamic
interactions. Proactive creation prepares phantom threads be-
fore pilot execution starts, while reactive creation spawns
phantom threads on-demand during runtime when pilot exe-
cution influence propagates to other original threads.
Proactive Creation. During PilotUtil.initNewExec, the PI-
LOT runtime library proactively pre-creates phantom worker
threads for known task executor patterns. We handle two
distinct implementations:
[I am still unsatisfied with how I present this two patterns]
First, for systems using third-party thread pools with standard
interfaces (e.g., Cassandra’s RepairJob submitted to Execu-
torService), PILOT provides a shared phantom thread pool
implementing the same standard interfaces. This phantom
pool is designed to serve multiple pilot execution rounds. Pi-
lot functions are instrumented to submit tasks to this phantom
pool instead of the original. When a task carrying PilotCon-
text is submitted (as instrumented in Section 4.1), it dynam-
ically propagates its specific PilotContext to the phantom
worker thread. This design allows the same phantom thread
pool to handle tasks from different pilot executions, with each
task bringing its own context.
Second, for systems with custom task executors using non-
standard interfaces, phantom threads are created specifically
for each pilot execution round. DuringPilotUtil.initNewExec,
PILOT creates a ZooKeeper node under /pilot-id that trig-
gers callbacks across all system nodes. These callbacks initial-
ize dedicated phantom threads with the current PilotContext
on each node, using the same constructor as original worker
threads but with separate task queues. Since these phantom
threads are pre-initialized with a specific PilotContext at cre-
ation time, they are dedicated to serving only the current pilot
execution round. Tasks submitted within pilot functions are
instrumented to route to these dedicated queues.
The key distinction between these two approaches stems
from interface compatibility constraints. For custom-interface
21

## Page 22

Conference’17, July 2017, Washington, DC, USA Submission # XXX
scenarios, phantom threads for customized workers are pre-
initialized with the assigned PilotContext when pilot exe-
cution starts, without relying on tasks to carry PilotCon-
text. This is because customized worker threads, despite
their customization, still implement the standard thread inter-
face, whereas task classes with non-standard interfaces lack
unified instrumentation patterns. In contrast, phantom thread
pools for standard interfaces receive PilotContext dynami-
cally, propagated from each submitted task. Finally, even if
extra phantom threads are created for unused worker types,
they remain idle and are safely reclaimed when pilot execu-
tion completes.
Reactive Creation. Phantom threads are also created reac-
tively at several key points during pilot execution. At the
entry point of pilot execution, the phantom thread is cre-
ated via PilotUtil.execute(pilotContext.wrap(recovery_-
entry_point())), which carries the PilotContext and exe-
cutes the pilot-version recovery entry function. At cross-
process communication interfaces, when the receiver side
detects PilotContext, phantom threads are spawned with the
received PilotContext to handle these pilot-originating re-
quests in isolation.
Micro-Fork for Synchronization and Shared State. The
most challenging scenario for reactive phantom thread cre-
ation is when original threads are influenced by pilot execu-
tion through synchronization primitives or shared state. We
introduce micro-fork, a lightweight mechanism that uses
static instrumentation at function invocation points to record
call stack-related information. At runtime, when an origi-
nal thread encounters a synchronization primitive or shared
variable marked with PilotContext as described in section
4.1, phantom threads are created on-demand. These phan-
tom threads fast-forward to reconstruct the call stack and
subsequently mimic the "influenced" effects in pilot version
functions.
Static instrumentation: PILOT uses interprocedural anal-
ysis to identify threads that may be influenced by pilot execu-
tion, specifically targeting long-running threads that contain
synchronization primitives or monitor shared states within
loops. In the motivating example, there is an Assignment-
Thread thread in HBase, which continuously waits on region
reassignment signals through cv.await() within its process-
ing loop. For such threads, we instrument all functions along
the multiple call paths leading to these potential influence
points—for example, one path is from run() through proces-
sAssignQueue() and waitOnAssignQueue() to cv.await(). Our
instrumentation inserts lightweight hooks that maintain con-
tinuous call stack checkpoints by pushing a frame before each
function invocation—recording the call site, target function,
and local variables—and popping the frame after the func-
tion returns. This ensures that when the AssignmentThread is
blocked at cv.await(), we have a complete snapshot of its call
stack.
Runtime execution: Based on context propagation, When
pilot execution triggers cv$wrapper.signal() to coordinate
AssignmentThread to finish the complex reassignment logic,
cv$wrapper.await() in original function detects the prop-
agated PilotContext and initiates micro-fork. A phantom
thread is spawned with the saved call stack [run →processAssignQueue →
waitOnAssignQueue → cv.await()] [TODO: add a figure to
better visualize micro fork]]. This phantom thread is ini-
tialized with the detected PilotContext and an additional
metadata flag included: isFastForward set to true. At the
beginning of each correponsindng pilot function of original
functions we identified are part of the call paths reaching
"influence point" in static instrumentation phase, if isFast-
Forward is true in phantom thread’s PilotContext, each pi-
lot function uses the recorded call sites to jump directly to
the next function in the stack, bypassing intermediate code.
For instance, when the phantom thread enters run$pilot(),
it checks the top frame to determine it should proceed to
processAssignQueue$pilot() at call site label 2, then jumps
directly there. Before entering each function, the system
restores local variables from the call stack through deep
copying and pops the corresponding frame. This process
repeats through run$pilot()->processAssignQueue$pilot()-
>waitOnAssignQueue$pilot() until the call stack is empty—
precisely at cv.await(). At this point, the isFastForward flag
is removed by instrumenting the pilot function, allowing
the phantom thread to execute the complex region assign-
ment logic entirely within the pilot version and also return
to normal pilot execution without any fast-forwarding.. This
approach ensures complete isolation: the original Assign-
mentThread remains blocked and unaffected, while the pilot
execution simulates the reassignment behavior.
State-level (❷) chang: similarly for this one To isolate state
modifications during pilot execution, a straightforward ap-
proach would be to create deep copies of all touched states.
However, this would double memory usage, making it im-
practical for production systems—especially for memory-
intensive operations in recovery, like Cassandra’s nodetool
repair, which deserializes large on-disk data chunks into
in-memory MerkleTrees.
Our key insight is that states touched in pilot execution
most of the time derive from fields of classes (except for
some reflection scenarios we cannot handle). Crucially, we
don’t need to copy entire object graphs because fields in
programming languages are organized as tree structures, and
pilot execution typically modifies only a small subset of nodes
in these trees.
Recursive Redirection to Shadow Fields PILOT there-
fore augments each class field with a corresponding shadow
field that serves as an isolated copy for pilot execution. These
shadow fields are by default set to null [TODO: Primitive
type field still incurs overhead since they have values by de-
fault] and incur no memory overhead when pilot execution is
22

## Page 23

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
not triggered. When pilot execution is triggered, we assigned
these shadow fields by only copying the reference of the orig-
inal fields—this suffices because modifications occur either
directly on fields or through their subfields, and our recursive
redirection mechanism ensures proper isolation. For instance,
when a pilot function modifies field and field.subfield,
modification is recursively redirected to its shadow coun-
terpart—field$shadow and field$shadow.subfield$shadow,
ensuring that no original field at any depth is ever modified.
This redirection also guarantees all local variables and method
parameters in pilot functions reference these shadow versions
instead of original fields. Importantly, memory overhead is
incurred only for the specific fields actually accessed during
pilot execution, not for the entire object graph. For the Cassan-
dra example, pilot execution assigns only a top-level shadow
field that holds references to the original MerkleTree structure
after shallow copying. The shadow fields in nested Merkle-
Tree nodes remain null since they are never accessed in pilot
execution, avoiding duplication of the entire tree structure.
Version Control for multi-round Pilot ExecutionSince
pilot execution may run multiple rounds, we need to differ-
entiate shadow field usage across rounds. PILOT augments
each field with an additional integer version field for version
control. Each pilot execution round carries a unique pilot
ID in PilotContext. PILOT instruments pilot function in a
way that, before accessing a field, if the current pilot ID is
larger than the field’s version number, PILOT performs a shal-
low copy from the original field and assigns to shadow field
plus updating the version to match the pilot ID. This ensures
each round gets its own clean shadow copy while reusing the
same shadow field storage—requiring only two additional
fields (shadow and version) to support multiple rounds of
pilot execution.
Tradeoff of accuracy and overhead Since shadow fields
capture a one-time snapshot, changes made by other threads
to original fields after the shallow copy won’t be reflected
in pilot execution. While continuously synchronizing these
changes would ensure accuracy, the overhead would be pro-
hibitive, and thus we sacrifice some accuracy for performance.
Special Handling For complex data structures(e.g., queues,
buffer pools), we implement customized copying strategies
beyond shallow copy. For instance, when copying a queue,
we create a new container structure without deep-copying
the individual items. For fields of imported package types
where we cannot instrument their internal implementation,
we perform deep cloning using specialized libraries [25]. To
further minimize overhead, we conduct immutability analy-
sis [60, 64] on these external fields—immutable fields require
no copying and can be accessed directly. [TODO: One further
optimization is that for some objects that are only created
temporarily in pilot execution, we don’t need to consider iso-
lation for them. For example, RepairManager is an object
created temporarily in Cassandra nodetool repair, and we
don’t need to consider any of its fields. Currently, I am using
thread1 
(phantom) 
thread1 
(original) 
message ﬁles 
3rd-party 
service 
thread2 
(phantom) 
(x’,y’) 
(x,y) 
➊ 
➋ ➌ 7➍
thread3 
(original) 
system.halt() 
Figure 8. Isolation across four levels: ❶ thread, ❷ in-memory state,
❸ I/O, and ❹ system actions. Observers in the pilot execution share
a collaborative view hidden from external observers.
a heuristic approach that is not sound: we recursively analyze
all non-static fields starting from the main class, as well as all
static fields. These fields are all the ones possibly subject to
modification. For the remaining fields, they are only likely to
be created temporarily, like RepairManager, so we can skip
shadow creation for them.]
I/O-level (❸) To isolate file system side effects during pilot
execution, PILOT intercepts all file operations and redirects
them to a dedicated shadow directory. Rather than eagerly
duplicating original files to shadow directory, PILOT employs
a lazy copying strategy: it initially replicates only the directory
structure and metadata, deferring actual data copying until
necessary.
This lazy copy optimization targets at scenarios where
recovery does not exhibit read-after-write behavior. When a
pilot writes to an existing file, PILOT avoids making a full
copy and instead appends changes to a separate log. Only if
the file is subsequently read during pilot execution does the
system reconstruct it by replaying the log over the original
content. For files that are only written but never read back, this
strategy significantly reduces I/O overhead. However, when a
read is triggered, we still have to pay the cost of copying the
original file and apply the append log on top of it.
Newly created files during pilot execution are written di-
rectly into the shadow environment. Since they have no pre-
existing version to preserve, no append log is used. Reads
simply access the latest content in the virtual file system,
maintaining isolation without extra overhead.
System-level (❹) Pilot version functions are sanitized to
remove dangerous actions such as system.halt(). Such op-
erations will be replaced with a reporting API to directly
registering such invocation in the system logs instead of exe-
cuting them in runtime.
ThirdParty-level As mentioned in Section 4.1, we provide a
proxy layer for third-party libraries. This proxy layer requires
some expertise for the third-party library. For now, we abstract
all the client-side operations of those third-party libraries into
read/write operations, and currently we implement such proxy
layer for HDFS and ZooKeeper. These proxies redirect all
operations to isolated namespaces under a pilot-specific prefix
(e.g., /pilot/...) that are only visible within pilot execution.
Since we treat these third-party services as file systems with
similar interfaces, the lazy copy optimization described above
23

## Page 24

Conference’17, July 2017, Washington, DC, USA Submission # XXX
Algorithm 2: Speculative Lock
1: State Variables:
2: lockSeq ← 0, currentHolder ← 0, delegate ← original lock
3:
4: procedure ACQUIRE_LOCK(t)
5: if t.state = ORIGINAL then
6: LOCK (delegate)
7: if lockSeq > currentHolder then
8: ABORT PILOT RUN()
9: else if t.state = PHANTOM then
10: t.mySeq ← lockSeq
11: lockSeq ← lockSeq +1
12: while (currentHolder < t.mySeq) ∨ ISLOCKED (delegate)
do
13: YIELD
14:
15: procedure RELEASE_LOCK(t)
16: if t.state = ORIGINAL then
17: UNLOCK (delegate)
18: else if t.state = PHANTOM then
19: currentHolder ← currentHolder + 1
for I/O isolation can also be applied to them, further reducing
the overhead.
A.2.2 Additional Handling
Concurrency and Speculative Locking. [TODO: This part
has not been finished yet] While shadow field redirection pro-
vides isolation for state modifications during pilot execution,
it introduces new concurrency challenges. When phantom
threads do shallow copy from original fields during state redi-
rection, race conditions can occur with concurrently executing
original threads. Additionally, multiple phantom threads may
conflict when accessing the same redirected state. A naive so-
lution would be to reuse existing locks during pilot execution,
ensuring proper synchronization. However, this approach is
risky because phantom threads acquiring the same locks as
original threads could potentially cause deadlock.
To avoid interfering with live execution, we introduce a
yield-based lock simulation mechanism (Algorithm 1). The
core principle is that phantom threads always yield to origi-
nal threads on conflict, immediately aborting pilot execution
when contention is detected. For synchronization among phan-
tom threads, we use a sequence-based protocol to simulate
lock semantics - each phantom thread registers its lock re-
quest and waits for its turn in the sequence without acquiring
original threads’ lock.
Manage the Lifecycle of Phantom Threads. The PILOT
runtime library is responsible for creating and managing all
phantom threads throughout their lifecycle. When pilot exe-
cution begins at PilotUtil.initNewExec, the runtime assigns
a globally unique ID and registers it in ZooKeeper under
/pilot-id/<id>. As phantom threads are spawned during pi-
lot execution, each thread registers itself under this ID names-
pace in ZooKeeper while simultaneously being tracked in
func2 
func1 
await 
original 
thread 
func1 
[var1, …] 
func2 
[var1, …] 
await 
[var1, …] 
stack 
func2’ 
func1’ 
await 
fast- 
forward 
micro-fork 
phantom 
thread 
f1 
f2 
a
reconstruct 
stack 
➊ 
➋
➌
Figure 9. Micro-fork
a local map maintained by the PILOT runtime library on
each node. PILOT also instruments these phantom threads to
remove their registrations from the namespace upon comple-
tion.
The entry point function blocks atPilotUtil.waitUntilFinished
(shown in Figure 4), which monitors the ZooKeeper names-
pace to detect pilot execution completion. This function waits
until all phantom thread registrations are removed from/pilot-
id/<id>, indicating that all phantom threads have finished and
the pilot execution has ended. For long-running or stuck phan-
tom threads, a timeout mechanism withinPilotUtil.waitUntilFinished
forcefully removes the pilot ID from ZooKeeper, triggering
cleanup callbacks across all nodes. These callbacks query
their local maps to terminate any remaining phantom threads
associated with that pilot execution ID, ensuring no threads
persist beyond their intended lifecycle.
Once PilotUtil.waitUntilFinished unblocks, execution
proceeds based on the recovery entry point type. For passive
recovery points, the original execution continues afterward,
as in our motivating example where the original recovery
resumes after pilot validation. For proactive recovery points,
the function returns directly without executing the original re-
covery, allowing operators to adjust recovery behavior based
on pilot execution feedback (e.g., modifying recovery param-
eters).
24

## Page 25

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
A.3 Observing and Reacting to Failures
Runtime Monitoring PILOT runtime embeds monitoring
components, which evaluate the effectiveness and impact
of recovery actions before deployment. To assess feasibil-
ity, the system checks if the same error persists during pi-
lot execution, indicating recovery failure. A timer measures
recovery duration and system downtime. Resource cost is
tracked through memory and I/O usage changes from check-
ers. For side effects, checkers detect new error signals and
monitor system health metrics, such as node availability and
request throughput, with support from existing runtime check-
ing tools [52, 74, 75].
Pilot Execution Tracing via Context Propagation Since
PILOT propagates PilotContext across threads and processes
involved in pilot execution (Section 4.1), we leverage this in-
frastructure to construct a complete execution trace. Drawing
from distributed tracing concepts [ 78, 79], we model pilot
execution as a tree of spans, where each span represents a
function execution within the pilot context. When a pilot
function begins, it creates a new span with a unique ID and
establishes parent-child relationships based on the call hier-
archy. This span metadata is stored within the PilotContext
and propagated alongside it.
When runtime monitors detect an anomaly—such as an
exception, timeout, or resource threshold violation—they reg-
ister the error with the current span ID. PILOT runtime library
then constructs the complete execution tree from the root
(pilot execution entry point) to the error location, capturing
the cross-component interactions.
Providing feedback to operator This trace provides oper-
ators with precise context: not just that recovery failed, but
the exact sequence of operations leading to the failure, in-
cluding which components were involved and how the error
propagated through the system. For example, operators could
know from the trace that crashes in HBase-25898 can be
avoided by simply skipping the empty but buggy WAL file.
The system could also perform iterative experimentation with
various recovery strategies and continuous refinement until
the underlying issues are fully resolved.
If PILOT reports a dry-run fails and recovery is invoked
manually, operators can tweak parameters or configurations—our
study shows that small adjustments (Finding 6) often resolve
the issue. For automated recovery, PILOT currently lacks a
mechanism to change the recovery behavior at runtime, but
surfacing the problem in advance is a crucial first step.Add
more A.4 Enabling Lightweight Pilot Execution
What
are
the
key
ideas?
Recovery should be prompt to reduce system downtime.
While it may seem advantageous to reduce actions during
pilot execution to accelerate recovery, we argue that this com-
promises the accuracy of the emulated results. Instead, we
propose reducing recovery delays by “warming up” the sys-
tem during pilot execution, enabling a rapid transition to
“fast replay” during actual recovery. We observe that bot-
tlenecks often stem from time-intensive operations such as
reading/writing large log files, transferring bulk data over
networks, and initializing new instances. Thus, we caches
intermediate results to mitigate these delays.
Caching IO Operations Recovery frequently requires trans-
ferring large data volumes between nodes. During pilot ex-
ecution, PILOT performs these transfers but stores them in
isolated locations. Upon committing recovery, we avoid re-
dundant transfers through checksum validation. Consider
Solr’s recovery example: when the operator tries to recover
a failed follower node, it must download files from leader
nodes through network stack to synchronize. During pilot
execution, the failed follower node downloads these files to
isolated directories and records checksums. When actual re-
covery begins, the node first query the remote checksum. If
unchanged, it simply rename the cached files from the isolated
directory to production paths—an O(1) operation replacing
network transfer. [This part is difficult to fully automatically
identify the code region that contains IO operations which are
cacheable, for now I manually change some code. ]
Caching Deterministic Computations Many recovery com-
putations are deterministic—given identical inputs, they pro-
duce identical outputs. PILOT mark functions as cacheable if
they have no side effects beyond return values, access only im-
mutable or versioned state, and contain no non-deterministic
operations. For Cassandra’s MerkleTree operations, the differ-
ence computation between two trees is purely functional—it
reads tree structures and produces a list of differing ranges
without modifying any state. During pilot execution, PILOT
computes a hash of the function’s inputs and stores the result
indexed by this hash. During actual recovery, if the input hash
matches, we return the cached result directly, eliminating
redundant computation.
[What is this part used for in old version? ]Isolation also
enables adopting more aggressive recovery strategies without
risking system stability. Developers often set conservative
failure detection thresholds to accommodate unstable cloud
environments [7, 30] adding to recovery delays. By leveraging
pilot execution, the system can preemptively begin recovery
operations, effectively masking this latency.
Design of Condition Variable. [For the implementation of
Condition Variable, please refer to Algorithm 5. CV is more
challenging since there are two goals for the wrapper: (1) En-
sure that CVs for phantom threads are separate from the orig-
inal delegate CV , which means we must simulate CV seman-
tics ourselves for phantom threads. Java’s LockSupport .park
and LockSupport .unpark are low level thread synchroniza-
tion primitives for blocking and waking threads, I used it to
implement the semantics of cv (2) CV , Semaphore, or Count-
DownLatch can proactively affect original threads, and the
wrapper should also be responsible for context propagation,
25

## Page 26

Conference’17, July 2017, Washington, DC, USA Submission # XXX
Algorithm 3: Speculative Lock
1: State Variables:
2: lockSeq ← 0, currentHolder ← 0, delegate ← original lock
3:
4: procedure ACQUIRE_LOCK(t)
5: if t.state = ORIGINAL then
6: LOCK (delegate)
7: if lockSeq > currentHolder then
8: ABORT PILOT RUN()
9: else if t.state = PHANTOM then
10: t.mySeq ← lockSeq
11: lockSeq ← lockSeq +1
12: while (currentHolder < t.mySeq) ∨ ISLOCKED (delegate)
do
13: YIELD
14:
15: procedure RELEASE_LOCK(t)
16: if t.state = ORIGINAL then
17: UNLOCK (delegate)
18: else if t.state = PHANTOM then
19: currentHolder ← currentHolder + 1
Algorithm 4: Speculative Lock
1: State Variables:
2: lockSeq ← 0, currentHolder ← 0, delegate ← original lock
3:
4: procedure ACQUIRE_LOCK(t)
5: if t.state = ORIGINAL then
6: LOCK (delegate)
7: if lockSeq > currentHolder then
8: ABORT PILOT RUN()
9: else if t.state = PHANTOM then
10: t.mySeq ← lockSeq
11: lockSeq ← lockSeq +1
12: while (currentHolder < t.mySeq) ∨ ISLOCKED (delegate)
do
13: YIELD
14:
15: procedure RELEASE_LOCK(t)
16: if t.state = ORIGINAL then
17: UNLOCK (delegate)
18: else if t.state = PHANTOM then
19: currentHolder ← currentHolder + 1
so the synchronization primitives discussed in Section 4.3.2
also rely on Algorithm 5.]
A.4.1 Handling Cross-Thread Patterns chang: consider
if we still want to preserve these five paragraphs, or summa-
rize them in the general approach framework; at least we need
to shrink the size The key insight for cross-thread propagation
is: they are in the same address space, thus we usually add
additional bookkeeping for shared data structures.
Task-Executor Model (❶). For asynchronous tasks submit-
ted to executor threads (e.g., RepairJob in Cassandra), we
instrument task classes that implement standard interfaces
Algorithm 5: Speculative Condition Variable
1: State Variables:
2: waitQueue ← / 0,delegate ← original CV
3:
4: procedure AW AIT(t, lock)
5: if t.state == ORIGINAL then
6: waitQueue.enqueue(t)
7: delegate.await() {Handles unlock/lock internally}
8: else if t.state ==PHANTOM then
9: waitQueue.enqueue(t)
10: UNLOCK (lock)
11: PARK THREAD (t)
12: LOCK (lock)
13:
14: procedure SIGNAL(t)
15: if t.state = ORIGINAL then
16: delegate.signal()
17: if ¬waitQueue.isEmpty() then
18: waitQueue.dequeue()
19: else if t.state = PHANTOM then
20: if ¬waitQueue.isEmpty() then
21: waiter ← waitQueue.dequeue()
22: if waiter.state == PHANTOM then
23: UNPARK THREAD (waiter)
24: else if waiter.state ==ORIGINAL then
25: MICRO FORK (waiter, t.pilotContext )
(Runnable, Future, Callable) by adding a PilotContext field.
When a task is submitted from a pilot function, PILOT instru-
ments it to carry the submitting thread’sPilotContext. PILOT
also instruments the task’s interface functions: if the Pilot-
Context contains a valid pilot ID, the task redirects to pilot-
version functions; otherwise, it executes normally. Therefore,
at runtime, if a task is created and submitted within a pilot
function, it will continue to redirect to pilot functions even
when executed in other threads. For custom task patterns (e.g.,
HBase’s recovery operations wrapped in a customized Proce-
dure class with self-implemented dedicated worker threads
using a queue-based SEDA design), we employ static data-
flow analysis from Panorama [ ? ] to identify such patterns
and ensure that tasks submitted in pilot mode execute with
dedicated pilot-aware worker threads that properly propagate
context (as detailed in Section 4.2).
Synchronization Primitives (❷). PILOT runtime library pro-
vides wrapper versions for commonly used synchronization
primitives (e.g., ConditionVariable, CountDownLatch), which
attach additional data structures to track the relationship
among threads and enable context propagation. PILOT instru-
ments the code to replace these synchronization primitives
with their wrapper versions. For example, a condition variable
wrapper( zhenyuPlease refer to Algorithm 5) maintains a wait
queue recording all waiting threads. When a phantom thread
signals, the wrapper dequeues the next waiter: if it’s an origi-
nal thread, it triggers micro-fork with the phantom thread’s
PilotContext to create an isolated execution environment for
26

## Page 27

Pilot Execution: Simulating Failure Recovery In Situfor Production Distributed Systems Conference’17, July 2017, Washington, DC, USA
that thread to continue in pilot mode. The wrapper’s wait
queue serves as the bridge for context propagation—when
the phantom thread signals, it can propagate its PilotContext
through this data structure to simulate the pilot execution’s in-
fluence on original threads via newly created phantom threads
from micro-fork. [For CountDownLatch or other synchroniza-
tion primitives, we could all provide a wrapper with a queue
to track waiting threads and enable context propagation.]
Shared Variable Monitoring ( ❸). For cases where orig-
inal threads monitor variables that pilot execution might
modify (e.g., while(a>0){...} where a could be changed
by pilot execution), potentially affecting original thread ex-
ecution, we use static analysis to identify such shared vari-
ables—typically those protected by locks or of concurrent
types. These variables are augmented with a separate Pi-
lotContext field. When pilot execution modifies such a vari-
able, it marks the variable with the currently executing pilot
function’s thread’s PilotContext. We instrument the code
by adding a conditional statement before each access to the
shared variable (e.g., if (a.$pilotContext contains valid
pilot ID) {redirect to pilot function...}). When an orig-
inal thread attempts to access a variable marked with pilot
context, this conditional check detects the pilot modification
and creates an isolated execution environment for the affected
code path (as described in Section 4.2). While we cannot
cover all such scenarios due to their complexity, our static
analysis focuses on simple, identifiable patterns with clear
data-flow dependencies and concurrency markers.
A.4.2 Handling Cross-Process/Service Patterns chang:
to add
Synchronous (❹). At RPC and HTTP send points, we seri-
alize the PilotContext from the sending thread into message
headers. Popular RPC/HTTP libraries provide straightfor-
ward interceptor mechanisms—HTTP frameworks offer .ad-
dHeader() methods and gRPC provides metadata injection
APIs—making instrumentation fully automatic. For systems
with custom cross-process protocols (e.g., HBase’s propri-
etary RPC framework), we extend their serialization logic to
include PilotContext with minimal effort, typically piggy-
backing on existing distributed tracing code that already prop-
agates metadata across processes. At the receiving-side entry
points, which are identifiable through well defined interfaces
(e.g., HTTP requests routed through doFilter() interface,
RPC interfaces defined in .proto files), AUTO PILOT adds
conditional logic: when a message contains PilotContext in
its header after deserialization, we refer to PILOT runtime lib
to create a dedicated thread to handle this pilot-originating
request. This thread inherits the PilotContext from the se-
rialized metadata in message header and executes the pilot
version of the handler functions.
Asynchronous (❺). For state update listeners on third-party
services (❸.b), PILOT propagates PilotContext by wrapping
the system’s usage of third-party client libraries with a proxy
layer. The third-party service remains unchanged—the proxy
sits between the system code and the third-party client li-
brary. Taking ZooKeeper as an example, when a pilot function
modify Zookeeper nodes through Zookeeper client, PILOT
replaces the client operation with a wrapper, intercepts this
call and performs additional bookkeeping: it serializes the
thread’s PilotContext to a metadata znode (e.g., /pilot/-
foo.pilot_context) . When a watch event fires, the proxy
intercepts the callback before it reaches application code, re-
trieves the stored PilotContext from the metadata znode, and
creates a new thread with this context to handle the event.
chang: do we support any callback function?
27