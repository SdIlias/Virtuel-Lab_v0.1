using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class final_state : FactoryBaseState
{
    public float speed = 1;
    bool isplayed = false;
    public override void EnterState(StateManager factory)
    {
        //Debug.Log("THE FINAL STATE entered at timestamp : " + Time.time);
    }
    public override void UpdateState(StateManager factory)
    {
        // le produit est transporter jusqu'au position4
        if (!isplayed)
            gameObject.transform.position = Vector3.MoveTowards(gameObject.transform.position, GameObject.FindWithTag("pos4").transform.position, speed * Time.deltaTime);
    }
    public override void OnCollisionEnter_(StateManager factory, Collider collision)
    {
        if ((collision.gameObject.name == "v-collider") && !isplayed)
        {
            // L'orsque le capteur detecte l'arrivé du produit le robot du transport transporte le package au stock
            GameObject.FindWithTag("balay").GetComponent<Animation>().Play("v translation");
            gameObject.GetComponent<Animation>().Play("v rotation");
            isplayed = true;
        }
        StartCoroutine(TillAnimCoroutine());
    }
    IEnumerator TillAnimCoroutine()
    {
        yield return new WaitForSeconds(2f);
        GameObject.FindWithTag("balay").GetComponent<Animation>().Play("v translation back");
        gameObject.GetComponent<Rigidbody>().useGravity = true;
    }
}
