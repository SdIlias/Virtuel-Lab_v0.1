using Unity.VisualScripting;
using UnityEngine;

public abstract class FactoryBaseState : MonoBehaviour
{
    // tous les etats herite de cette class les 3 methodes suivants:
    public abstract void EnterState(StateManager factory);
    public abstract void UpdateState(StateManager factory); 
    public abstract void OnCollisionEnter_(StateManager factory , Collider collision);
}
